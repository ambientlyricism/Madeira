#!/usr/bin/env python3
"""Library front end: launch profiles, controller navigation and the session
exit report.

1. Swift: compiles the production LibraryEntry and LibraryController
   (app/Madeira/Library.swift) with small stubs and checks the launch
   environment a profile exports (executable, arguments, desktop size, CPU
   cores, synchronisation), profile validation, decoding of library files that
   carry unknown keys, and the pad-to-command mapping.
2. C: compiles the session exit hooks from app/Madeira/WineProcessBridge.m and
   checks the program counters, the helper-image filter, the last error status
   and MADEIRA_EXIT_REPORT=0.
3. Source checks: ntdll reports program starts and exits to those hooks, and
   the app wires the library into ContentView and GamepadInput.

Run from anywhere; needs `swift` and `cc` on PATH.
"""
from pathlib import Path
import re
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[2]
lib = (root / 'app/Madeira/Library.swift').read_text()
bridge = (root / 'app/Madeira/WineProcessBridge.m').read_text()
server = (root / 'build/ntdll-unix/server_ios.c').read_text()
content = (root / 'app/Madeira/ContentView.swift').read_text()
gamepad = (root / 'app/Madeira/GamepadInput.swift').read_text()
failures = []


def check(cond, what):
    print(('PASS: ' if cond else 'FAIL: ') + what)
    if not cond:
        failures.append(what)


def block(text, header):
    p = text.index(header)
    a = text.index('{', p)
    n, b = 1, a + 1
    while n:
        n += (text[b] == '{') - (text[b] == '}')
        b += 1
    return text[p:b]


swift = r'''
import Foundation
#if canImport(Combine)
import Combine
#else
// Linux hosts: just enough of Combine for LibraryController.
protocol ObservableObject: AnyObject {}
@propertyWrapper struct Published<Value> { var wrappedValue: Value; init(wrappedValue: Value) { self.wrappedValue = wrappedValue } }
final class AnyCancellable { init() {} }
final class PassthroughSubject<Output, Failure: Error> {
    private var receivers: [(Output) -> Void] = []
    func send(_ value: Output) { receivers.forEach { $0(value) } }
    func sink(receiveValue: @escaping (Output) -> Void) -> AnyCancellable { receivers.append(receiveValue); return AnyCancellable() }
}
#endif
enum MadeiraConfig { static func flag(_ name: String, fallback: Bool = true) -> Bool { fallback } }
func madeira_set_vsync_locked(_ mode: Int32) {}
struct TouchControl: Codable, Equatable { var nx = 0.5 }
enum LibraryError: LocalizedError { case message(String) }
func env(_ name: String) -> String? { getenv(name).map { String(cString: $0) } }
'''
swift += block(lib, 'struct LibraryEntry: Codable, Identifiable') + '\n'
swift += block(lib, 'final class LibraryController: ObservableObject, @unchecked Sendable') + '\n'
swift += r'''
var failed = 0
func expect(_ cond: Bool, _ what: String) { print((cond ? "PASS: " : "FAIL: ") + what); if !cond { failed += 1 } }

// Desktop entry: services in a virtual desktop of the chosen size.
var desk = LibraryEntry.desktopEntry
desk.resolution = "1280x720"
expect(desk.launchArguments == "/desktop=shell,1280x720 C:\\windows\\system32\\services.exe", "desktop arguments")
desk.configureLaunch()
expect(env("MADEIRA_EXE") == "explorer.exe" && env("MADEIRA_DESKTOP") == "1", "desktop starts explorer in desktop mode")
expect(env("MADEIRA_SCREEN_W") == "1280" && env("MADEIRA_SCREEN_H") == "720", "desktop size exported")

// A direct game: its Windows path and arguments; no desktop state left over.
var game = LibraryEntry(title: "Game", relativePath: "Games/Some Game/bin/game.exe", bits: 32)
game.arguments = "-windowed \"-name=a b\""
game.configureLaunch()
expect(env("MADEIRA_EXE") == "C:\\Games\\Some Game\\bin\\game.exe", "direct executable path")
expect(env("MADEIRA_ARGS") == "-windowed \"-name=a b\"", "direct arguments verbatim")
expect(env("MADEIRA_DESKTOP") == nil && env("MADEIRA_SCREEN_W") == nil, "desktop state cleared")

game.cpuCount = 4; game.fastSync = false; game.semaphoreFastPath = true; game.reducedX87 = false
game.applyEnvironment()
expect(env("MADEIRA_CPU_COUNT") == "4", "CPU cores exported")
expect(env("MADEIRA_FASTSYNC") == "0" && env("MADEIRA_FASTSYNC_SEM") == "1", "synchronisation choices exported")
expect(env("FEX_X87REDUCEDPRECISION") == "0", "x87 precision exported")
game.cpuCount = nil; game.fastSync = true; game.semaphoreFastPath = nil
game.applyEnvironment()
expect(env("MADEIRA_CPU_COUNT") == nil, "automatic cores leave MADEIRA_CPU_COUNT unset")
expect(env("MADEIRA_FASTSYNC") == "auto" && env("MADEIRA_FASTSYNC_SEM") == "0", "default synchronisation")

// Validation.
expect((try? game.validate()) != nil, "a normal profile validates")
var bad = game; bad.arguments = "\"unbalanced"
expect((try? bad.validate()) == nil, "unbalanced quotes refused")
bad = game; bad.arguments = (0..<65).map { "a\($0)" }.joined(separator: " ")
expect((try? bad.validate()) == nil, "more than 64 arguments refused")
bad = game; bad.resolution = "10x10"
expect((try? bad.validate()) == nil, "invalid size refused")
bad = game; bad.fpsMode = 7
expect((try? bad.validate()) == nil, "invalid frame limit refused")

// Library files: unknown keys (fields a newer or older build wrote) are ignored.
let json = """
{"id":"AF046C35-C32A-497B-92BC-0BBD14F8CB62","title":"T","relativePath":"a/b.exe","bits":64,"arguments":"",
 "resolution":"1024x768","fpsMode":3,"reducedX87":true,"fastSync":true,"liveLogs":false,"performance":false,
 "touchControls":true,"someNewerKey":42,"display":"fit","cpuCount":2}
"""
let decoded = try? JSONDecoder().decode(LibraryEntry.self, from: Data(json.utf8))
expect(decoded?.fpsMode == 3 && decoded?.cpuCount == 2 && decoded?.touchControls == true, "decodes a file with unknown keys")

// Controller navigation.
let c = LibraryController.shared
var got: [String] = []
let sub = c.commands.sink { got.append($0) }
func pump() { RunLoop.main.run(until: Date().addingTimeInterval(0.05)) }
c.configure(enabled: true, ownsInput: true)
c.sample(buttons: 0x0001, lx: 0, ly: 0); c.sample(buttons: 0, lx: 0, ly: 0)
c.sample(buttons: 0, lx: 30000, ly: 0); c.sample(buttons: 0, lx: 0, ly: 0)
c.sample(buttons: 0x1000, lx: 0, ly: 0); c.sample(buttons: 0, lx: 0, ly: 0)
pump()
expect(got == ["up", "right", "accept"], "library owns input: d-pad, stick and A navigate (\(got))")
expect(c.ownsInput, "library owns input")
got = []
c.configure(enabled: true, ownsInput: false)
c.sample(buttons: 0x0010, lx: 0, ly: 0); c.sample(buttons: 0, lx: 0, ly: 0)
c.sample(buttons: 0x0030, lx: 0, ly: 0); c.sample(buttons: 0, lx: 0, ly: 0)
pump()
expect(got == ["menu"], "in a session only Back+Start opens the menu (\(got))")
expect(!c.ownsInput, "the game owns input in a session")
got = []
c.configure(enabled: false, ownsInput: true)
c.sample(buttons: 0x1000, lx: 0, ly: 0); pump()
expect(got.isEmpty && !c.ownsInput, "developer interface: no navigation")
_ = sub
exit(failed == 0 ? 0 : 1)
'''

c_src = r'''
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
'''
start = bridge.index('static uint64_t g_crash_exit')
end = bridge.index('static char *g_prefix_path')
c_src += bridge[start:end]
c_src += r'''
static int failed;
static void expect(int cond, const char *what) { printf("%s: %s\n", cond ? "PASS" : "FAIL", what); if (!cond) failed++; }
int main(void) {
    uint32_t status = 0;
    unsetenv("MADEIRA_EXIT_REPORT");
    wine_exit_status_reset(); wine_programs_reset();
    wine_process_did_start("explorer.exe"); wine_process_did_start("services.exe");
    expect(wine_programs_started() == 0, "helper images are not programs");
    wine_process_did_start("Game.exe"); wine_process_did_start("launcher.exe");
    expect(wine_programs_started() == 2 && wine_programs_live() == 2, "two programs started");
    wine_process_did_exit("launcher.exe", 0);
    expect(wine_programs_live() == 1 && !wine_crash_exit_status(&status), "clean exit: no report");
    wine_process_did_exit("CMD.EXE", (int)0xC0000005);
    expect(!wine_crash_exit_status(&status), "a helper's error is not the game's");
    wine_process_did_exit("Game.exe", (int)0xC0000005);
    expect(wine_crash_exit_status(&status) && status == 0xC0000005u, "the game's error status is recorded");
    expect(wine_programs_live() == 0, "all programs ended");
    wine_process_did_exit("Game.exe", 0);
    expect(wine_programs_live() == 0, "live count never goes negative");
    wine_exit_status_reset();
    expect(!wine_crash_exit_status(&status), "reset clears the status");
    setenv("MADEIRA_EXIT_REPORT", "0", 1);
    wine_process_did_exit("Game.exe", (int)0xC0000017);
    expect(!wine_crash_exit_status(&status), "MADEIRA_EXIT_REPORT=0 records nothing");
    wine_process_did_exit(NULL, (int)0xC0000017);
    return failed ? 1 : 0;
}
'''

with tempfile.TemporaryDirectory() as tmp:
    sp = Path(tmp) / 'frontend.swift'
    sp.write_text(swift)
    r = subprocess.run(['swift', str(sp)], capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.returncode:
        sys.stdout.write(r.stderr[-4000:])
        failures.append('swift harness')
    cp = Path(tmp) / 'exit.c'
    cp.write_text(c_src)
    exe = Path(tmp) / 'exit'
    r = subprocess.run(['cc', '-std=c11', '-Wall', '-Werror', '-D_DEFAULT_SOURCE', '-o', str(exe), str(cp)],
                       capture_output=True, text=True)
    if r.returncode:
        sys.stdout.write(r.stderr[-4000:])
        failures.append('C harness build')
    else:
        r = subprocess.run([str(exe)], capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        if r.returncode:
            failures.append('C harness')

done = block(server, 'void server_init_process_done(void)')
check('ios_notify_process_start();' in done, 'ntdll reports each program start')
check('wine_process_did_exit( name, status )' in block(server, 'static void ios_notify_process_exit( int status )'),
      'ntdll reports each program exit with its status')
check(re.search(r'if \(!c \|\| c > 127\) return FALSE;', server) is not None, 'non-ASCII image names are not reported')
check('LibraryView(play: launchLibraryEntry' in content, 'ContentView shows the library when it is the chosen interface')
check('runWineFullSequence(profile: entry)' in content and 'profile.applyEnvironment()' in content,
      'library launches use the shared launch path with the profile applied')
check('Button("Use New Interface")' in content, 'the developer interface can switch back to the library')
check('LibraryController.shared' in gamepad and 'library.ownsInput' in gamepad,
      'player 1 pad drives the library and is neutral while the library owns input')
print('check-frontend:', 'FAIL' if failures else 'PASS')
sys.exit(1 if failures else 0)
