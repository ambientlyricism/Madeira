import Foundation

/// ml1095: ONE configuration file for every runtime switch: Documents/madeira.cfg
///
///     # comments start with #
///     key = value        (whitespace trimmed; the value runs to the end of the
///                         line, so it may contain '='; the last line wins)
///
/// Keys are the old per-file names without "madeira-" and ".txt"
/// (swap-mb, vram-mb, pool, totalphys, wx, ...). Environment exports are
/// "env.NAME = value". DXMT options are one line, "dxmt = a=b;c=d".
///
/// The native side reads the same file through build/madeira_cfg.h with the
/// same rules. When madeira.cfg is ABSENT the legacy one-value-per-file layout
/// still works; when it is PRESENT the legacy files are ignored, so the one
/// file is the single source of truth. `migrateLegacy()` writes madeira.cfg
/// from whatever legacy files exist, once, so they can then be deleted. A
/// madeira-env.txt supplied after that is imported into the existing file,
/// and a legacy file is deleted only once its value is verified in it.
enum MadeiraConfig {
    static let fileName = "madeira.cfg"

    /// Every switch that used to live in its own Documents/madeira-<key>.txt.
    static let legacyKeys = [
        "swap-mb", "swap-canary", "vram-mb", "pool", "totalphys", "inproc-sync", "wx",
        "mono-bridge", "ctx-frame", "tf-trace", "usd-time", "real-suspend", "mono-suspend",
        "arena", "arena-mb", "arena-test", "fexfail", "remote", "remote-batch", "d3d12",
        "apicensus", "shadow", "census", "wxprobe", "args", "valley-args",
        "jumbo-mb", "jumbo-keep-mb", "iat-noexec", "vmwatch", "no-local-read", "vsps-fill",
    ]

    static var documents: URL? {
        FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first
    }
    static var url: URL? { documents?.appendingPathComponent(fileName) }
    static var present: Bool { url.map { FileManager.default.fileExists(atPath: $0.path) } ?? false }

    /// All key/value pairs of madeira.cfg (empty when the file is absent).
    static func all() -> [String: String] {
        guard let u = url, let text = try? String(contentsOf: u, encoding: .utf8) else { return [:] }
        var out: [String: String] = [:]
        for raw in text.split(omittingEmptySubsequences: false, whereSeparator: { $0 == "\n" || $0 == "\r\n" }) {
            let line = raw.trimmingCharacters(in: .whitespaces)
            if line.isEmpty || line.hasPrefix("#") { continue }
            guard let eq = line.firstIndex(of: "=") else { continue }
            let k = line[..<eq].trimmingCharacters(in: .whitespaces)
            let v = line[line.index(after: eq)...].trimmingCharacters(in: .whitespaces)
            if !k.isEmpty { out[k] = v }
        }
        return out
    }

    /// The value for `key`, trimmed, or nil when unset. Falls back to the legacy
    /// file ONLY when madeira.cfg does not exist.
    static func get(_ key: String) -> String? {
        if present { return all()[key] }
        guard let d = documents,
              let txt = try? String(contentsOf: d.appendingPathComponent("madeira-\(key).txt"), encoding: .utf8)
        else { return nil }
        return txt.trimmingCharacters(in: .whitespacesAndNewlines)
    }

    static func bool(_ key: String, default dflt: Bool = false) -> Bool {
        guard let v = get(key) else { return dflt }
        return ["1", "on", "true", "yes"].contains(v)
    }

    /// A runtime kill switch read on the Swift side, spelled like the native
    /// ones: `env.NAME = 0` in madeira.cfg or `NAME=0` in madeira-env.txt (the
    /// latter wins until migrateLegacy has imported it), else the process
    /// environment, else `fallback`. Any value other than "0" means on. The same
    /// line is also exported to the guest by WineProcessBridge, so one switch
    /// covers both halves.
    static func flag(_ name: String, fallback: Bool = true) -> Bool {
        if let v = environmentValues()[name] { return v != "0" }
        return getenv(name).map { String(cString: $0) != "0" } ?? fallback
    }

    /// The environment exports as the next launch will see them: madeira.cfg's
    /// `env.NAME` lines, overlaid with a madeira-env.txt that has not been
    /// imported yet. Only MADEIRA_* and DXMT_* names are accepted.
    static func environmentValues() -> [String: String] {
        var values: [String: String] = [:]
        for (key, value) in all() where key.hasPrefix("env.") {
            let name = String(key.dropFirst(4))
            if allowedEnvironmentName(name) { values[name] = value }
        }
        if let d = documents, let text = try? String(contentsOf: d.appendingPathComponent("madeira-env.txt"), encoding: .utf8) {
            values.merge(parseEnvironment(text)) { _, latest in latest }
        }
        return values
    }

    static func allowedEnvironmentName(_ name: String) -> Bool {
        (name.hasPrefix("MADEIRA_") || name.hasPrefix("DXMT_")) &&
            name.utf8.allSatisfy { (65...90).contains($0) || (97...122).contains($0) || (48...57).contains($0) || $0 == 95 }
    }

    /// KEY=VALUE lines of madeira-env.txt; the last line for a name wins.
    static func parseEnvironment(_ text: String) -> [String: String] {
        var result: [String: String] = [:]
        for raw in text.split(whereSeparator: { $0.isNewline }) {
            let line = raw.trimmingCharacters(in: .whitespaces)
            guard !line.hasPrefix("#"), let eq = line.firstIndex(of: "=") else { continue }
            let name = line[..<eq].trimmingCharacters(in: .whitespaces)
            let value = line[line.index(after: eq)...].trimmingCharacters(in: .whitespaces)
            if allowedEnvironmentName(name), !value.contains("\0") { result[name] = value }
        }
        return result
    }

    /// With madeira.cfg present, a madeira-env.txt supplied later is imported
    /// instead of being ignored: the values that differ are appended as
    /// `env.NAME = value` lines (existing keys and comments are kept) and read
    /// back before the import counts. `env.MADEIRA_CONFIG_ENV_MERGE = 0` (or the
    /// same line in madeira-env.txt) keeps the file unimported, and therefore
    /// undeleted. Returns the names imported.
    @discardableResult
    static func mergeLegacyEnvironment(log: (String) -> Void) -> [String] {
        guard let d = documents, let u = url, present,
              environmentValues()["MADEIRA_CONFIG_ENV_MERGE"] != "0",
              let text = try? String(contentsOf: d.appendingPathComponent("madeira-env.txt"), encoding: .utf8),
              let original = try? String(contentsOf: u, encoding: .utf8) else { return [] }
        let values = parseEnvironment(text), current = all()
        let changed = values.keys.filter { current["env." + $0] != values[$0] }.sorted()
        guard !changed.isEmpty else { return [] }
        do {
            let suffix = changed.map { "env.\($0) = \(values[$0]!)" }.joined(separator: "\n")
            try (original + "\n# Environment overrides imported from madeira-env.txt\n" + suffix + "\n")
                .write(to: u, atomically: true, encoding: .utf8)
            guard changed.allSatisfy({ all()["env." + $0] == values[$0] }) else { return [] }
            log("[config-env] imported \(changed.count) environment override(s) from madeira-env.txt into madeira.cfg")
            return changed
        } catch {
            log("[config-env] import into madeira.cfg failed; madeira-env.txt is kept")
            return []
        }
    }

    /// One-time migration: with no madeira.cfg and at least one legacy file,
    /// write madeira.cfg from them. Legacy files are left in place (ignored from
    /// now on) so nothing is destroyed; the log names them so they can be deleted.
    /// Returns the keys that were migrated. With madeira.cfg already present it
    /// only imports a newer madeira-env.txt (mergeLegacyEnvironment).
    @discardableResult
    static func migrateLegacy(log: (String) -> Void) -> [String] {
        if present { return mergeLegacyEnvironment(log: log) }
        guard let d = documents, let u = url, !present else { return [] }
        var lines = ["# Madeira configuration (ml1095): one file for every switch.",
                     "# key = value; lines starting with # are comments; the last line wins.",
                     "# Keys are the old file names without 'madeira-' and '.txt'.",
                     "# Environment exports: env.NAME = value. DXMT options: dxmt = a=b;c=d.",
                     ""]
        var migrated: [String] = []
        for key in legacyKeys {
            guard let txt = try? String(contentsOf: d.appendingPathComponent("madeira-\(key).txt"), encoding: .utf8) else { continue }
            let v = txt.trimmingCharacters(in: .whitespacesAndNewlines)
            lines.append("\(key) = \(v)")
            migrated.append(key)
        }
        if let txt = try? String(contentsOf: d.appendingPathComponent("madeira-dxmt.txt"), encoding: .utf8) {
            let parts = txt.split(whereSeparator: { $0 == "\n" || $0 == "\r\n" })
                .map { $0.trimmingCharacters(in: .whitespaces) }.filter { !$0.isEmpty && !$0.hasPrefix("#") }
            if !parts.isEmpty { lines.append("dxmt = " + parts.joined(separator: ";")); migrated.append("dxmt") }
        }
        if let txt = try? String(contentsOf: d.appendingPathComponent("madeira-env.txt"), encoding: .utf8) {
            for raw in txt.split(whereSeparator: { $0 == "\n" || $0 == "\r\n" }) {
                let line = raw.trimmingCharacters(in: .whitespaces)
                guard !line.isEmpty, !line.hasPrefix("#"), let eq = line.firstIndex(of: "="), eq != line.startIndex else { continue }
                lines.append("env.\(line[..<eq]) = \(line[line.index(after: eq)...])")
            }
            migrated.append("env")
        }
        guard !migrated.isEmpty else { return [] }
        do {
            try (lines.joined(separator: "\n") + "\n").write(to: u, atomically: true, encoding: .utf8)
            log("madeira.cfg written from legacy files (\(migrated.joined(separator: ", "))); the madeira-*.txt files are now ignored and can be deleted")
        } catch {
            log("madeira.cfg could not be written: \(error)")
            return []
        }
        return migrated
    }

    /// Once madeira.cfg exists the legacy files are dead weight: remove every
    /// known switch file (never logs, traces or the input map) whose values
    /// madeira.cfg is verified to hold. A file that could not be imported, or
    /// that disagrees with madeira.cfg, is kept. Idempotent.
    /// Returns the names removed.
    @discardableResult
    static func deleteLegacyFiles(log: (String) -> Void) -> [String] {
        guard present, let d = documents else { return [] }
        var removed: [String] = []
        for name in legacyKeys.map({ "madeira-\($0).txt" }) + ["madeira-env.txt", "madeira-dxmt.txt"] {
            let u = d.appendingPathComponent(name)
            guard FileManager.default.fileExists(atPath: u.path) else { continue }
            // madeira.cfg existing is no proof that this file's values are in it.
            guard let text = try? String(contentsOf: u, encoding: .utf8) else { continue }
            let stored = all()
            if name == "madeira-env.txt" {
                let values = parseEnvironment(text)
                guard !values.isEmpty, values.allSatisfy({ stored["env." + $0.key] == $0.value }) else { continue }
            } else if name == "madeira-dxmt.txt" {
                let value = text.split(whereSeparator: { $0.isNewline }).map { $0.trimmingCharacters(in: .whitespaces) }
                    .filter { !$0.isEmpty && !$0.hasPrefix("#") }.joined(separator: ";")
                guard stored["dxmt"] == value else { continue }
            } else {
                let key = String(name.dropFirst("madeira-".count).dropLast(4))
                guard stored[key] == text.trimmingCharacters(in: .whitespacesAndNewlines) else { continue }
            }
            do { try FileManager.default.removeItem(at: u); removed.append(name) }
            catch { log("could not remove \(name): \(error)") }
        }
        if !removed.isEmpty { log("removed legacy config files (madeira.cfg is the one file now): " + removed.joined(separator: ", ")) }
        return removed
    }
}
