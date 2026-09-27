#!/usr/bin/env python3
"""Library front end: launch profiles, controller navigation and the session
exit report.

1. Swift: compiles the production LibraryEntry and LibraryController
   (app/Madeira/Library.swift) and the display layout (app/Madeira/
   GuestDisplay.swift) with small stubs and checks the launch environment a
   profile exports (executable, arguments, virtual monitor size for every
   entry, D3D9 anisotropy, CPU cores, synchronisation), profile validation,
   decoding of library files that carry unknown or fork-written keys (display
   mode, control opacity and size), the layout and touch-mapping math of every
   Aspect & scaling mode, and the pad-to-command mapping.
2. C: compiles the session exit hooks from app/Madeira/WineProcessBridge.m and
   checks the program counters, the helper-image filter, the last error status
   and MADEIRA_EXIT_REPORT=0.
3. Source checks: ntdll reports program starts and exits to those hooks; the
   app wires the library into ContentView and GamepadInput; game details offer
   Resolution (with Screen shape) for every entry, Aspect & scaling, D3D9
   anisotropy and control opacity/size; the in-game menu offers Aspect &
   scaling, opacity, size and the Touch pointer mode; and a session saves
   those choices to the game.

Run from anywhere; needs `swift` and `cc` on PATH.
"""
from pathlib import Path
import re
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[2]
lib = (root / 'app/Madeira/Library.swift').read_text()
display = (root / 'app/Madeira/GuestDisplay.swift').read_text()
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
final class LogStore { static let shared = LogStore(); var lines: [String] = []; func log(_ s: String) { lines.append(s) } }
var published: (Int32, Int32) = (0, 0)
func winios_display_mode_changed(_ w: Int32, _ h: Int32) { published = (w, h) }
func madeira_set_vsync_locked(_ mode: Int32) {}
struct TouchControl: Codable, Equatable { var nx = 0.5 }
enum LibraryError: LocalizedError { case message(String) }
func env(_ name: String) -> String? { getenv(name).map { String(cString: $0) } }
enum SteamPaths {
    static func safeRelative(_ path: String, under root: URL) -> URL? { path.isEmpty ? nil : root.appendingPathComponent(path) }
    static func validAppID(_ value: Int) -> Bool { value > 0 && UInt64(value) <= UInt64(UInt32.max) }
}
enum SteamFileError: Error { case invalid(String) }
enum LibraryModel { static var drive = URL(fileURLWithPath: "/tmp/madeira-frontend-check") }
'''
swift += block(lib, 'struct LibraryEntry: Codable, Identifiable') + '\n'
swift += '\n'.join(l for l in display.splitlines() if not l.startswith('import ')) + '\n'
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
expect(published == (1280, 720), "desktop size published to the display shim")

// A direct game: its Windows path and arguments; no desktop state left over.
var game = LibraryEntry(title: "Game", relativePath: "Games/Some Game/bin/game.exe", bits: 32)
game.arguments = "-windowed \"-name=a b\""
game.configureLaunch()
expect(env("MADEIRA_EXE") == "C:\\Games\\Some Game\\bin\\game.exe", "direct executable path")
expect(env("MADEIRA_ARGS") == "-windowed \"-name=a b\"", "direct arguments verbatim")
expect(env("MADEIRA_DESKTOP") == nil, "desktop state cleared")
// Every entry's Resolution becomes the session's virtual monitor.
expect(game.resolution == "1280x720", "new entries default to 1280x720")
expect(env("MADEIRA_SCREEN_W") == "1280" && env("MADEIRA_SCREEN_H") == "720" && env("MADEIRA_SCREEN_SRC") == "knob",
       "a direct game's resolution is exported as the session default")
game.resolution = "1560x720"; game.configureLaunch()
expect(env("MADEIRA_SCREEN_W") == "1560" && env("MADEIRA_SCREEN_H") == "720" && published == (1560, 720),
       "a screen-shape resolution is exported and published")
expect((try? game.validate()) != nil, "a screen-shape resolution validates")
game.resolution = "1280x720"; game.configureLaunch()

game.cpuCount = 4; game.fastSync = false; game.semaphoreFastPath = true; game.reducedX87 = false
game.applyEnvironment()
expect(env("MADEIRA_CPU_COUNT") == "4", "CPU cores exported")
expect(env("MADEIRA_FASTSYNC") == "0" && env("MADEIRA_FASTSYNC_SEM") == "1", "synchronisation choices exported")
expect(env("FEX_X87REDUCEDPRECISION") == "0", "x87 precision exported")
expect(env("DXMT_D9_ANISO_LIMIT") == "0", "anisotropy: application default")
game.anisotropyLimit = 8; game.applyEnvironment()
expect(env("DXMT_D9_ANISO_LIMIT") == "8", "D3D9 anisotropy limit exported")
expect(LogStore.shared.lines.last == "[display-shape] resolution=1280x720 mode=fit", "the profile's display shape is logged")
game.anisotropyLimit = nil
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
expect(decoded?.displayMode == .fit && decoded?.controlOpacity == nil && decoded?.anisotropyLimit == nil, "older files: Fit, default controls")
// Written by the fork's app: display mode, control opacity/size, anisotropy.
let fork = """
{"id":"AF046C35-C32A-497B-92BC-0BBD14F8CB63","title":"T","relativePath":"a/b.exe","bits":32,"arguments":"",
 "resolution":"1560x720","display":"aspect","fpsMode":1,"reducedX87":true,"fastSync":true,"liveLogs":false,
 "performance":false,"touchControls":false,"controlOpacity":0.4,"controlSize":1.5,"anisotropyLimit":4,"extendedModes":false}
"""
let forked = try? JSONDecoder().decode(LibraryEntry.self, from: Data(fork.utf8))
expect(forked?.displayMode == .aspect && forked?.resolution == "1560x720", "display mode and resolution decode")
expect(forked?.controlOpacity == 0.4 && forked?.controlSize == 1.5 && forked?.anisotropyLimit == 4, "control opacity/size and anisotropy decode")
var odd = forked!; odd.display = "sideways"
expect(odd.displayMode == .fit, "an unknown display mode falls back to Fit")
let saved = try? JSONEncoder().encode(forked!)
let again = saved.flatMap { try? JSONDecoder().decode(LibraryEntry.self, from: $0) }
expect(again?.display == "aspect" && again?.controlSize == 1.5, "the profile encodes its display and control choices")

// Layout: the presented rect and the touch mapping for each mode.
let guest = CGSize(width: 1280, height: 720), view = CGRect(x: 0, y: 0, width: 844, height: 390)
func near(_ a: CGFloat, _ b: CGFloat) -> Bool { abs(a - b) < 0.5 }
let fit = GameSurfaceLayout.rect(guest: guest, bounds: view, mode: .fit)
expect(near(fit.height, 390) && near(fit.width, 693.3) && near(fit.minX, 75.3), "Fit letterboxes at the guest's shape")
let fill = GameSurfaceLayout.rect(guest: guest, bounds: view, mode: .fill)
expect(near(fill.width, 844) && near(fill.height, 474.75) && fill.minY < 0, "Fill covers the view and crops")
expect(GameSurfaceLayout.rect(guest: guest, bounds: view, mode: .stretch) == view, "Stretch is the view")
let drawn = CGSize(width: 1024, height: 768)
let aspect = GameSurfaceLayout.rect(guest: guest, aspect: drawn, bounds: view, mode: .aspect)
expect(near(aspect.width / aspect.height * 3, 4) && near(aspect.height, 390), "Aspect follows the drawn shape")
expect(GameSurfaceLayout.rect(guest: guest, bounds: view, mode: .aspect) == fit, "Aspect is Fit until a frame is drawn")
let tall = GameSurfaceLayout.rect(guest: guest, aspect: CGSize(width: 2560, height: 720), bounds: view, mode: .fitHeight)
expect(near(tall.height, 390) && tall.width > view.width, "Fill height keeps the full height")
let centre = GameSurfaceLayout.map(point: CGPoint(x: 422, y: 195), guest: guest, bounds: view, mode: .fit)
expect(near(centre.x, 640) && near(centre.y, 360), "the centre maps to the guest's centre")
let bar = GameSurfaceLayout.map(point: CGPoint(x: 10, y: 10), guest: guest, bounds: view, mode: .fit)
expect(bar.x == 0 && near(bar.y, 18.5), "a touch in the letterbox clamps to the edge")
let corner = GameSurfaceLayout.map(point: CGPoint(x: 844, y: 390), guest: guest, bounds: view, mode: .stretch)
expect(corner.x == 1279 && corner.y == 719, "mapping clamps to the last guest pixel")
let phone = GuestDisplay.defaultMode(forLandscapeView: CGSize(width: 844, height: 390))
let tablet = GuestDisplay.defaultMode(forLandscapeView: CGSize(width: 1024, height: 768))
expect(phone.w == 1280 && phone.h == 720, "phone default mode is 1280x720")
expect(tablet.w == 1152 && tablet.h == 864, "4:3 default mode is 1152x864 (cheapest 4:3 of at least 0.9 MP)")
expect(DisplayMode.allCases.map { $0.label } == ["Fit", "Fill", "Stretch", "Aspect", "Fill height"], "the five Aspect & scaling choices")

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
check('runWineFullSequence(profile: entry' in content and 'profile.applyEnvironment(' in content,
      'library launches use the shared launch path with the profile applied')
check('Button("Use New Interface")' in content, 'the developer interface can switch back to the library')
check('LibraryController.shared' in gamepad and 'library.ownsInput' in gamepad,
      'player 1 pad drives the library and is neutral while the library owns input')

# The options restored from the fork's app.
detail = block(lib, 'struct LibraryDetail: View')
hud = block(lib, 'struct LibraryHUD: View')
model = block(lib, 'final class LibraryModel: ObservableObject')
check('Picker("Resolution", selection: $entry.resolution)' in detail and 'Desktop size' not in lib,
      'game details: one Resolution picker for every entry (not only the Desktop)')
check('screenShapeResolution' in detail and 'Text("Screen shape (' in detail and 'MADEIRA_SCREEN_SHAPE_RESOLUTION' in detail,
      'game details: Screen shape resolution choice')
check('Picker("Aspect & scaling"' in detail and 'entry.display = $0' in detail, 'game details: Aspect & scaling')
check('Picker("D3D9 anisotropic filtering"' in detail and 'entry.anisotropyLimit' in detail, 'game details: D3D9 anisotropy')
check('LabeledContent("Control opacity")' in detail and 'LabeledContent("Control size")' in detail,
      'game details: control opacity and size sliders')
check('Picker("Aspect & scaling", selection: $model.displayMode)' in hud and 'MADEIRA_SESSION_TOOLS' in hud,
      'in-game menu: Aspect & scaling (MADEIRA_SESSION_TOOLS)')
check('LabeledContent("Opacity")' in hud and 'LabeledContent("Size")' in hud, 'in-game menu: control opacity and size')
check('Text("Touch").tag("touch")' in lib and 'input.touchMode = value == "touch"' in lib,
      'pointer settings: Absolute, Relative and Touch')
save = block(model, 'func saveCurrentProfile()')
check('entry.display = displayMode.rawValue' in save and 'entry.controlOpacity = opacity' in save
      and 'entry.controlSize = controls.sizeScale' in save, 'a session saves display mode, opacity and size to the game')
begin = block(model, 'func begin(_ entry: LibraryEntry')
check('displayMode = entry.displayMode' in begin and 'controls.sizeScale =' in begin and 'opacity =' in begin,
      "a session starts with the game's display mode, opacity and size")
check('GuestDisplay.configureSessionDefault(' in block(lib, 'func configureLaunch('),
      'every launch sets the virtual monitor from the Resolution')
check('GameSurfaceLayout.rect(' in content and 'GameSurfaceLayout.map(' in content and 'effectiveDisplayMode()' in content
      and '* 1024 / r.width' not in content, 'the game view lays out and maps touches through GameSurfaceLayout')
check('if touchPointerMode { touchModeBegan(touches); return }' in content, 'the game view handles the Touch pointer mode')
check('TouchControlsModel.diameter(control)' in content and 'library.opacity' in content,
      "touch controls follow the session's size and opacity")
print('check-frontend:', 'FAIL' if failures else 'PASS')
sys.exit(1 if failures else 0)
