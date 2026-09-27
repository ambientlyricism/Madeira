#!/usr/bin/env python3
"""Compile the production JIT-pool sizing (StikJITHelper.swift) on the host.

The early-pool sizing lines of prepareEarlyPool are compiled verbatim with the remembered
size, madeira.cfg pool and the pressure record stubbed, together with JITPoolPolicy. Checks:
explicit madeira.cfg pool > remembered size or the 896 MB default, raised to the pressure
floor; the session pool; the remembered size with and without MADEIRA_POOL_STICKY_MAX; the
pressure step (896, then 1152); and that the session records its size for the next run.
Needs a Swift toolchain (SWIFTC, default swiftc).
"""
from pathlib import Path
import os
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
helper = (root / 'app/Madeira/StikJITHelper.swift').read_text()
content = (root / 'app/Madeira/ContentView.swift').read_text()
policy = helper[helper.index('enum JITPoolPolicy {'):]

early = helper[helper.index('static func prepareEarlyPool('):]
early = early[early.index('earlyInFlight = true') + len('earlyInFlight = true'):
              early.index('LogStore.shared.log("[jit-early] ml1330 trigger=')]
assert 'JITPoolPolicy.afterPressure(usedMB: max(used, floor))' in helper
assert 'MadeiraConfig.flag("MADEIRA_POOL_STICKY_MAX")' in helper and '"madeiraLastPoolMB"' in helper
remembered = helper[helper.index('static var rememberedPoolMB: Int? {'):]
assert 'JITPoolPolicy.validMB.contains(mb) ? mb : nil' in remembered[:remembered.index('\n    }')]
session = content[content.index('let explicitPoolMB = StikJITHelper.explicitPoolMB'):]
session = session[:session.index('StikJITHelper.allocatePool(poolSize: poolSizeMB * 1024 * 1024)')]
assert 'JITPoolPolicy.sessionPoolMB(explicit: explicitPoolMB,' in session
assert 'pressureFloorMB: StikJITHelper.poolPressureFloorMB)' in session
assert 'StikJITHelper.rememberSessionPool(sizeMB: poolSizeMB, explicit: explicitPoolMB != nil)' in session

checks = r'''
var rememberedPoolMB: Int? = nil
var explicitPoolMB: Int? = nil
var pressure = 0
func consumePoolPressure() -> Int { pressure }
func earlyPool(remembered: Int?, explicit: Int?, pressureMB: Int) -> (Int, String) {
    rememberedPoolMB = remembered; explicitPoolMB = explicit; pressure = pressureMB
''' + early + r'''
    return (sizeMB, source)
}
@main struct Checks {
    static func main() {
        typealias P = JITPoolPolicy
        // early pool
        precondition(earlyPool(remembered: nil, explicit: nil, pressureMB: 0) == (896, "default"))
        precondition(earlyPool(remembered: 512, explicit: nil, pressureMB: 0).0 == 512, "recent sessions")
        precondition(earlyPool(remembered: 1152, explicit: nil, pressureMB: 0).0 == 1152)
        precondition(earlyPool(remembered: 512, explicit: nil, pressureMB: 896).0 == 896, "pressure floor")
        precondition(earlyPool(remembered: 1152, explicit: nil, pressureMB: 896).0 == 1152)
        precondition(earlyPool(remembered: 1152, explicit: 384, pressureMB: 1152) == (384, "madeira.cfg pool"))
        // session pool
        precondition(P.sessionPoolMB(explicit: nil, pressureFloorMB: 0) == 896)
        precondition(P.sessionPoolMB(explicit: nil, pressureFloorMB: 1152) == 1152)
        precondition(P.sessionPoolMB(explicit: 512, pressureFloorMB: 1152) == 512)
        // remembered size
        precondition(P.rememberedMB(session: 896, explicit: false, previous: 1152, sticky: true) == 1152, "largest")
        precondition(P.rememberedMB(session: 896, explicit: false, previous: 1152, sticky: false) == 896, "last")
        precondition(P.rememberedMB(session: 512, explicit: true, previous: 1152, sticky: true) == 512, "explicit")
        precondition(P.rememberedMB(session: 896, explicit: false, previous: 0, sticky: true) == 896)
        precondition(P.rememberedMB(session: 896, explicit: false, previous: 9999, sticky: true) == 896)
        precondition(!P.validMB.contains(0) && !P.validMB.contains(4096) && P.validMB.contains(512))
        // pressure step
        precondition(P.afterPressure(usedMB: 512) == 896 && P.afterPressure(usedMB: 895) == 896)
        precondition(P.afterPressure(usedMB: 896) == 1152 && P.afterPressure(usedMB: 1152) == 1152)
        print("PASS: early/session pool sizing, sticky and last-session memory, explicit override, pressure floor")
    }
}
'''
with tempfile.TemporaryDirectory(prefix='madeira-pool-check-') as directory:
    folder = Path(directory)
    source = folder / 'Checks.swift'
    source.write_text(policy + '\n' + checks)
    executable = folder / 'check'
    subprocess.run([os.environ.get('SWIFTC', 'swiftc'), '-parse-as-library',
                    str(source), '-o', str(executable)], check=True)
    subprocess.run([str(executable)], check=True)
