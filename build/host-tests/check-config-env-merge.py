#!/usr/bin/env python3
"""Exercise the production madeira.cfg migration and Swift-side flag lookup on disk.

Compiles app/Madeira/MadeiraConfig.swift with Documents redirected to a temporary folder
and checks: a madeira-env.txt supplied after madeira.cfg exists is honoured before the
launch imports it and after, the import keeps existing keys and comments, is idempotent
and only allows MADEIRA_*/DXMT_* names, a legacy file is deleted only once its value is
verified in madeira.cfg, MADEIRA_CONFIG_ENV_MERGE=0 keeps the file (and its values), and a
madeira.cfg that cannot be read never costs the only copy of a switch.
Needs a Swift toolchain (SWIFTC, default swiftc).
"""
from pathlib import Path
import os
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
config = (root / 'app/Madeira/MadeiraConfig.swift').read_text().replace(
    'FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first',
    'URL(fileURLWithPath: CommandLine.arguments[1])')
checks = r'''
import Foundation
func require(_ value: @autoclosure () -> Bool, _ label: String) {
    precondition(value(), label)
}
@main struct Checks {
    static func main() throws {
        let d = MadeiraConfig.documents!, cfg = MadeiraConfig.url!
        let legacy = d.appendingPathComponent("madeira-env.txt")
        func write(_ text: String, _ url: URL) throws { try text.write(to: url, atomically: true, encoding: .utf8) }
        // An existing madeira.cfg, then a newly supplied madeira-env.txt: the
        // switch must hold for the UI before the launch imports the file, and
        // after the import has deleted it.
        try write("# keep this comment\nenv.MADEIRA_OTHER = 1\npool = 7\n", cfg)
        try write("# trial\nMADEIRA_EXAMPLE = 0\nMADEIRA_EXAMPLE=1\nDXMT_TEST = a=b\nPATH=/bad\n", legacy)
        require(MadeiraConfig.flag("MADEIRA_EXAMPLE", fallback: false), "override seen before the import")
        MadeiraConfig.migrateLegacy(log: { _ in })
        MadeiraConfig.deleteLegacyFiles(log: { _ in })
        require(!FileManager.default.fileExists(atPath: legacy.path), "verified import allows cleanup")
        require(MadeiraConfig.flag("MADEIRA_EXAMPLE", fallback: false), "override kept after the import")
        require(MadeiraConfig.all()["pool"] == "7", "unrelated config preserved")
        require(MadeiraConfig.all()["env.MADEIRA_OTHER"] == "1", "existing env line preserved")
        let saved = try String(contentsOf: cfg, encoding: .utf8)
        require(saved.contains("# keep this comment"), "comments preserved")
        require(MadeiraConfig.environmentValues()["DXMT_TEST"] == "a=b", "embedded equals preserved")
        require(MadeiraConfig.environmentValues()["PATH"] == nil, "loader environment excluded")
        MadeiraConfig.migrateLegacy(log: { _ in })
        let repeated = try String(contentsOf: cfg, encoding: .utf8)
        require(saved == repeated, "repeat migration is idempotent")
        try write("MADEIRA_EXAMPLE=0\n", legacy)
        require(!MadeiraConfig.flag("MADEIRA_EXAMPLE"), "explicit off before the import")
        MadeiraConfig.migrateLegacy(log: { _ in })
        MadeiraConfig.deleteLegacyFiles(log: { _ in })
        require(!MadeiraConfig.flag("MADEIRA_EXAMPLE"), "explicit off after the import")
        try write("MADEIRA_EXAMPLE=1\nMADEIRA_CONFIG_ENV_MERGE=0\n", legacy)
        MadeiraConfig.migrateLegacy(log: { _ in })
        MadeiraConfig.deleteLegacyFiles(log: { _ in })
        require(FileManager.default.fileExists(atPath: legacy.path), "an unimported file is never deleted")
        require(MadeiraConfig.flag("MADEIRA_EXAMPLE"), "the kept file still applies")
        try write("9", d.appendingPathComponent("madeira-pool.txt"))
        MadeiraConfig.deleteLegacyFiles(log: { _ in })
        require(FileManager.default.fileExists(atPath: d.appendingPathComponent("madeira-pool.txt").path),
                "a legacy value that disagrees with madeira.cfg is kept")
        try write("7", d.appendingPathComponent("madeira-pool.txt"))
        MadeiraConfig.deleteLegacyFiles(log: { _ in })
        require(!FileManager.default.fileExists(atPath: d.appendingPathComponent("madeira-pool.txt").path),
                "a legacy value madeira.cfg holds is deleted")
        // A madeira.cfg that cannot be read must not lose the only copy of a switch.
        try FileManager.default.removeItem(at: cfg)
        try FileManager.default.createDirectory(at: cfg, withIntermediateDirectories: false)
        try write("MADEIRA_EXAMPLE=1\n", legacy)
        MadeiraConfig.migrateLegacy(log: { _ in })
        MadeiraConfig.deleteLegacyFiles(log: { _ in })
        require(FileManager.default.fileExists(atPath: legacy.path), "failed import keeps madeira-env.txt")
        require(MadeiraConfig.flag("MADEIRA_EXAMPLE"), "and its switch still applies")
        print("PASS: env overrides after madeira.cfg exists, import, verified cleanup, rollback, failure retention")
    }
}
'''
with tempfile.TemporaryDirectory(prefix='madeira-config-check-') as directory:
    folder = Path(directory)
    source = folder / 'Checks.swift'
    source.write_text(config + '\n' + checks)
    docs = folder / 'Documents'
    docs.mkdir()
    executable = folder / 'check'
    subprocess.run([os.environ.get('SWIFTC', 'swiftc'), '-parse-as-library',
                    str(source), '-o', str(executable)], check=True)
    subprocess.run([str(executable), str(docs)], check=True)
