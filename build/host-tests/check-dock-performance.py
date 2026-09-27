#!/usr/bin/env python3
"""Compile production pool/diagnostic policy, including desktop recovery cases,
and the Dock session's 32-bit heap, CPU and address-space diagnostic defaults."""
from pathlib import Path
import shutil
import subprocess, tempfile

root = Path(__file__).resolve().parents[2]
source = (root / 'app/Madeira/MadeiraDock.swift').read_text(encoding='utf-8')
start = source.index('enum DockPerformancePolicy {')
policy = source[start:source.index('\n}', start) + 2]
helper_source = (root / 'app/Madeira/StikJITHelper.swift').read_text(encoding='utf-8')
jit_policy_start = helper_source.index('enum JITPoolPolicy {')
policy += '\n' + helper_source[jit_policy_start:helper_source.index('\n}', jit_policy_start) + 2]
tests = r'''
import Foundation
import Glibc
func early(_ legacy: Int = 896, _ explicit: Int? = nil, _ dock: Bool = true,
           _ compact: Bool = true, _ setup: Bool = true, _ desktop: Bool = false) -> Int {
    DockPerformancePolicy.earlyPoolMB(legacy: legacy, explicit: explicit,
        dock: dock, compact: compact, setupComplete: setup, desktopReserved: desktop)
}
assert(early() == 512)
assert(early(1152) == 512) // obsolete setup/sticky desktop high-water
assert(early(1152, nil, true, true, false) == 1152) // unfinished onboarding
assert(early(896, nil, false) == 896) // legacy client route
assert(early(896, nil, true, false) == 896) // rollback
assert(early(512, nil, true, true, true, true) == 896) // desktop recovery
assert(early(1152, nil, true, true, true, true) == 1152)
for override in [256, 512, 640, 896, 1152] {
    assert(early(896, override) == override)
    assert(early(896, override, true, true, true, true) == override)
    assert(!DockPerformancePolicy.needsDesktopRestart(compactPoolMB: 512,
        explicit: override, desktop: true, dock: false))
}
assert(DockPerformancePolicy.needsDesktopRestart(compactPoolMB: 512,
    explicit: nil, desktop: true, dock: false))
for size in [0, 896, 1152] {
    assert(!DockPerformancePolicy.needsDesktopRestart(compactPoolMB: size,
        explicit: nil, desktop: true, dock: false))
}
assert(!DockPerformancePolicy.needsDesktopRestart(compactPoolMB: 512,
    explicit: nil, desktop: true, dock: true))
assert(!DockPerformancePolicy.needsDesktopRestart(compactPoolMB: 512,
    explicit: nil, desktop: false, dock: false))
for dock in [false, true] { for light in [false, true] {
    for diagnostic in [false, true] { for forensic in [false, true] {
        let value = DockPerformancePolicy.censusDefault(dock: dock, lightweight: light,
            diagnostic: diagnostic, forensic: forensic)
        assert(value == (dock && light && !diagnostic && !forensic ? "0" : nil))
        // The real launch block only installs a default into an unset variable.
        setenv("MADEIRA_D3D9_CENSUS", "1", 1)
        if let value { setenv("MADEIRA_D3D9_CENSUS", value, 0) }
        assert(String(cString: getenv("MADEIRA_D3D9_CENSUS")) == "1")
    }}
}}
// ml1880: a Dock session's pool is compact, raised to the pressure floor.
assert(DockPerformancePolicy.compactSessionPoolMB(pressureFloorMB: 0) == 512)
assert(DockPerformancePolicy.compactSessionPoolMB(pressureFloorMB: 896) == 896)
assert(DockPerformancePolicy.compactSessionPoolMB(pressureFloorMB: 1152) == 1152)
assert(DockPerformancePolicy.compactSessionPoolMB(pressureFloorMB: 100) == 512)
print("PASS: compact/setup/rollback/explicit sizing, desktop recovery, diagnostic overrides")
'''
content = (root / 'app/Madeira/ContentView.swift').read_text(encoding='utf-8')
launch = content[content.index('private func runWineFullSequence('):]
assert launch.index('reserveDesktopPoolIfNeeded') < launch.index('ws_log_quiet = 1')
assert 'getenv("MADEIRA_D3D9_CENSUS") == nil' in launch
assert 'setenv("MADEIRA_D3D9_CENSUS", value, 0)' in launch
assert launch.index('censusDefault(') < launch.index('startWineProcess()')
# ml1880: the session pool of a Dock launch is compact and is what the next run remembers.
session = launch[launch.index('let explicitPoolMB = StikJITHelper.explicitPoolMB'):]
assert 'let compactDock = dock && MadeiraConfig.flag("MADEIRA_DOCK_COMPACT_POOL")' in session
assert session.index('DockPerformancePolicy.compactSessionPoolMB(') < session.index('StikJITHelper.rememberSessionPool(')
assert 'compactDock && explicitPoolMB == nil' in session, 'an explicit madeira.cfg pool wins over the compact size'
assert session.index('StikJITHelper.rememberSessionPool(') < session.index('StikJITHelper.allocatePool(poolSize: poolSizeMB')
assert 'rememberCompactPool(sizeMB: pool.size / 1024 / 1024, selected: compactDock)' in session
# ml1940/ml1950: a Dock session's heap, CPU and address-space defaults; each explicit =0 stays.
heap_names = ['MADEIRA_HEAP_COMPACT', 'MADEIRA_HEAP_COMBINED', 'MADEIRA_HEAP_RECLAIM',
              'MADEIRA_HEAP_STATS', 'MADEIRA_CPU_DIAGNOSTICS', 'MADEIRA_VA_DIAGNOSTICS']
heap_start = launch.index('            if dock {\n                setenv("MADEIRA_HEAP_COMPACT", "1", 0)')
heap_block = launch[heap_start:launch.index('\n            }\n', heap_start) + len('\n            }\n')]
for name in heap_names:
    assert f'setenv("{name}", "1", 0)' in heap_block, name
assert heap_start < launch.index('startWineProcess()')
heap_program = r'''
import Foundation
import Glibc
final class LogFixture { var lines: [String] = []; func log(_ line: String) { lines.append(line) } }
let logStore = LogFixture()
func applyDockDefaults(dock: Bool) {
BLOCK
}
let names = NAMES
for name in names { unsetenv(name) }
applyDockDefaults(dock: false)
for name in names { assert(getenv(name) == nil, name) }
assert(logStore.lines.isEmpty)
applyDockDefaults(dock: true)
for name in names { assert(String(cString: getenv(name)) == "1", name) }
assert(logStore.lines.contains { $0.hasPrefix("[dock-heap] ml1940 compact=1") })
assert(logStore.lines.contains { $0.contains("[dock-diagnostics] ml1950") && $0.contains("va=1") })
for name in names {
    for other in names { unsetenv(other) }
    setenv(name, "0", 1)
    applyDockDefaults(dock: true)
    for other in names { assert(String(cString: getenv(other)) == (other == name ? "0" : "1"), other) }
}
print("PASS: Dock heap, CPU and address-space defaults; explicit =0 overrides kept; none outside Dock")
'''.replace('BLOCK', heap_block).replace('NAMES', '[' + ', '.join(f'"{n}"' for n in heap_names) + ']')
jit = (root / 'app/Madeira/StikJITHelper.swift').read_text(encoding='utf-8')
assert 'UserDefaults.standard.set(true, forKey: desktopPoolKey)' in jit
assert 'if sizeMB >= 896 { UserDefaults.standard.removeObject(forKey: desktopPoolKey) }' in jit
assert 'DockPerformancePolicy.earlyPoolMB' in jit
begin = jit.index('    private static let desktopPoolKey')
end = jit.index('    // ml1330/ml1420: the early pool is taken at app start', begin)
pool_methods = jit[begin:end]
fixtures = r'''
final class DefaultsFixture {
    var values: [String: Bool] = [:]
    var ints: [String: Int] = [:]
    func set(_ value: Bool, forKey key: String) { values[key] = value }
    func set(_ value: Int, forKey key: String) { ints[key] = value }
    func removeObject(forKey key: String) { values.removeValue(forKey: key); ints.removeValue(forKey: key) }
    func bool(forKey key: String) -> Bool { values[key] ?? false }
    func integer(forKey key: String) -> Int { ints[key] ?? 0 }
}
enum UserDefaults { static let standard = DefaultsFixture() }
enum MadeiraConfig {
    static var override: String?
    static var off: Set<String> = []
    static func get(_ key: String) -> String? { override }
    static func flag(_ key: String, fallback: Bool = true) -> Bool { !off.contains(key) }
}
final class LogStore { static let shared = LogStore(); func log(_ value: String) {} }
enum PoolHarness {
    static var poolReady = false
    METHODS
}
'''.replace('METHODS', pool_methods)
tests += r'''
let key = "madeiraDockDesktopPoolNextRun"
assert(!PoolHarness.reserveDesktopPoolIfNeeded(desktop: true, dock: false))
PoolHarness.rememberCompactPool(sizeMB: 512, selected: true)
PoolHarness.poolReady = true
assert(!PoolHarness.reserveDesktopPoolIfNeeded(desktop: true, dock: true))
assert(PoolHarness.reserveDesktopPoolIfNeeded(desktop: true, dock: false))
assert(UserDefaults.standard.bool(forKey: key))
// A failed/undersized allocation must not consume the next-run reservation.
PoolHarness.rememberCompactPool(sizeMB: 768, selected: false)
assert(UserDefaults.standard.bool(forKey: key))
PoolHarness.rememberCompactPool(sizeMB: 896, selected: false)
assert(!UserDefaults.standard.bool(forKey: key))
MadeiraConfig.override = "640"
assert(!PoolHarness.reserveDesktopPoolIfNeeded(desktop: true, dock: false))
MadeiraConfig.override = " 512\n"
assert(PoolHarness.explicitPoolMB == 512)
MadeiraConfig.override = "255"
assert(PoolHarness.explicitPoolMB == nil)
MadeiraConfig.override = "invalid"
assert(PoolHarness.explicitPoolMB == nil)
// ml2000: pool-pressure feedback.
assert(DockPerformancePolicy.earlyPoolMB(legacy: 512, explicit: nil, dock: true, compact: true,
       setupComplete: true, desktopReserved: false, pressureMB: 896) == 896)
assert(DockPerformancePolicy.earlyPoolMB(legacy: 512, explicit: 640, dock: true, compact: true,
       setupComplete: true, desktopReserved: false, pressureMB: 1152) == 640)
assert(DockPerformancePolicy.earlyPoolMB(legacy: 896, explicit: nil, dock: false, compact: true,
       setupComplete: true, desktopReserved: false, pressureMB: 1152) == 1152)
assert(DockPerformancePolicy.earlyPoolMB(legacy: 512, explicit: nil, dock: true, compact: true,
       setupComplete: true, desktopReserved: false, pressureMB: 100) == 512)
assert(JITPoolPolicy.afterPressure(usedMB: 512) == 896)
assert(JITPoolPolicy.afterPressure(usedMB: 896) == 1152)
assert(JITPoolPolicy.afterPressure(usedMB: 1152) == 1152)
UserDefaults.standard.set(896, forKey: "madeiraPoolPressureMB")
assert(PoolHarness.poolPressureFloorMB == 896)
MadeiraConfig.off = ["MADEIRA_POOL_FEEDBACK"]
assert(PoolHarness.poolPressureFloorMB == 0 && PoolHarness.consumePoolPressure() == 0)
MadeiraConfig.off = []
print("PASS: production reservation persistence, successful-allocation consumption, manual overrides and ml2000 pool-pressure floor")
'''
with tempfile.TemporaryDirectory(prefix='madeira-perf-') as folder:
    folder = Path(folder)
    (folder / 'main.swift').write_text(tests + '\n' + policy + '\n' + fixtures, encoding='utf-8')
    subprocess.run([shutil.which('swiftc') or 'swiftc', str(folder / 'main.swift'),
                    '-o', str(folder / 'check')], check=True)
    subprocess.run([str(folder / 'check')], check=True)
    (folder / 'heap.swift').write_text(heap_program, encoding='utf-8')
    subprocess.run([shutil.which('swiftc') or 'swiftc', str(folder / 'heap.swift'),
                    '-o', str(folder / 'heap')], check=True)
    subprocess.run([str(folder / 'heap')], check=True)
