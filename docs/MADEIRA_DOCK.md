# Madeira Dock

Madeira Dock is a small headless host for **Valve's genuine Windows Steam
client**. Instead of running the full desktop client (its Chromium web helper,
library UI and ~100 threads) next to a game, Dock loads the client's own
libraries inside Madeira's Wine session, signs in with the user's own account,
and asks the client to launch the game with Valve's own `LaunchApp`. The
client's online authentication and license checks decide whether the game
starts; the game's executable, its Steam API calls and any DRM stay exactly as
Valve ships them. Dock contains no Steam emulator, no DRM bypass, no ticket
forging and no game patches.

It is an optional route for Steam games started from the library
(`docs/STEAM.md`); "Steam (more usage)" in a game's Start with picker keeps the
regular desktop client, and `MADEIRA_DOCK=0` turns Dock off entirely.

## What is in this repository

- `app/Madeira/arm64ec-windows/dockhost.exe`: the stripped Dock executable
  (x64 PE, 37,888 bytes, SHA-256
  `ea6c56a4dcfee525c48f07abaa896fb6b4bdc080cda90aa937b28e590a015c6e`),
  started as `C:\windows\system32\dockhost.exe`.
- `app/Madeira/arm64ec-windows/dock-notices.txt`: its binary licence and the
  LLVM and MinGW-w64 runtime notices it needs.
- `app/Madeira/MadeiraDock.swift`: the public app-side contract: routing,
  validation, the one-use sign-in transfer, the host's environment, the
  numeric report parser and its messages, and the performance policy.
- The Dock parts of `Library.swift`, `ContentView.swift`, `SteamAccount.swift`,
  `SteamFiles.swift` (install scripts), `SteamRuntime.swift` (component
  setup), `Onboarding.swift`, `StikJITHelper.swift` and `WineProcessBridge.m`.

**The Dock source is not here and is not open source.** It is maintained in a
private repository by 125hz. The executable is distributed under the Madeira
Dock licence in `dock-notices.txt` (distribution of unmodified releases with
Madeira is permitted); it is therefore not under this repository's
GPL-3.0-or-later and Converter Exception. No Valve files, game content or
developer login are bundled: the user installs Valve's client files and signs
in at runtime.

## How a Dock launch works

1. **Route.** A Steam game that starts through the client uses Dock when Dock
   is enabled (`MadeiraDock.routes`). Dock supports Steam's default launch
   option (imported default arguments count as default; custom arguments are
   refused rather than silently dropped) and needs the client's components
   (`steamclient64.dll`) in drive_c.
2. **Sign-in hand-off.** Madeira pauses its downloads, closes its own Steam
   connection, reads the refresh token from the Keychain and writes a bounded
   one-use transfer (account name, token, SteamID and App ID; format
   `MDOCK001`) to `Application Support/MadeiraDock/launch.auth`: complete file
   protection, 0600, excluded from backups, created exclusively. Only its path
   enters the guest environment (`MADEIRA_DOCK_AUTH_FILE`, through Wine's
   `\\?\unix` namespace, so no drive mapping is assumed). Dock consumes and
   deletes it before authenticating; Madeira removes any leftover when the
   session ends, on sign-out and at the next start. Nothing in it is an
   ownership claim: only Valve accepting the token establishes identity.
3. **One-time installs.** Valve's client never runs install scripts on this
   route, so Madeira does: runtimes its Wine provides (DirectX, Visual C++,
   .NET) are marked done; other programs not yet recorded done run once in the
   Dock session, from a batch, before the host (`DockInstallScripts`).
4. **Custom executables.** When the install record lists per-user custom
   executables (`CheckGuid`), Dock asks Valve's client to prepare them before
   it launches (`MADEIRA_STEAM_HOST_CEG`). The client does this itself.
5. **Launch and status.** The session runs `dockhost.exe` in a Wine desktop.
   Dock writes numeric stages to `C:\madeira-dock.txt`; Madeira reads only
   whitelisted numeric fields and a client fingerprint (`MadeiraDock.parseReport`)
   and turns known failures (unsupported client build, no license, Valve's own
   launch refusal codes, custom-executable preparation errors) into messages.
   The host's exit status reaches the app through ntdll's exit hook. The
   starting screen shows what Dock waits for (content Valve is installing, the
   one-time installs) until the game's window is up.
6. **Session end.** Dock's desktop outlives the host; once the host has exited
   and every program the session started has ended for 5 s, the session ends as
   if Quit had been tapped, keeping the exit report.

## Setup

With Dock on, first-run setup signs in first and then prepares Valve's client
components natively (`SteamRuntime.swift`, about 73 MB): three pinned client
packages are downloaded from Valve's update CDN (HTTPS,
`client-update.akamai.steamstatic.com` only), checked against pinned sizes and
SHA-256 sums, and unpacked into `C:\Program Files (x86)\Steam`; the unpacked
`steamclient64.dll` must match the build Dock's adapter was validated against
(pins never follow a moving client manifest). The prefix is seeded from the
bundled template and Steam's registry keys are written, all without starting
Wine. Existing Steam files are kept. The desktop installer
remains available ("Use desktop setup instead"). Settings › Windows Steam client
can install and boot the regular desktop client as a fallback.

## Performance policy

- **Compact JIT pool.** A Dock session has no desktop client/CEF fan-out
  (device sessions used about 230 MB of code), so with Dock on and setup done
  the early pool is 512 MB instead of 896 MB, raised to the floor an earlier
  dry pool set (`madeira-pool-pressure.txt`). A desktop session in the same
  app run stops before Wine starts and reserves 896 MB for the next run (the
  pool cannot grow once the debugger has detached). An explicit `pool` in
  madeira.cfg always wins.
- **Diagnostics.** A Dock session keeps frame and memory telemetry but turns
  the per-call D3D9 census off by default (over 32,000 calls per frame were
  counted); `MADEIRA_D3D9_CENSUS=1`, `MADEIRA_DIAG` or `MADEIRA_D3D9_LAST`
  keep it.
- **32-bit heaps.** A Dock session turns on the bounded 32-bit heap policies
  (`MADEIRA_HEAP_COMPACT`, `_COMBINED`, `_RECLAIM`) and their statistics; each
  can be set to 0.

## Switches

`env.NAME = 0` in `Documents/madeira.cfg`. All default on unless noted.

| Switch | `0` means |
| --- | --- |
| `MADEIRA_DOCK` | no Dock: Steam games start through the desktop client |
| `MADEIRA_DOCK_NATIVE_SETUP` | setup uses the desktop installer |
| `MADEIRA_DOCK_UNIX_HANDOFF` | the transfer path uses `Z:` instead of `\\?\unix` |
| `MADEIRA_DOCK_DEFAULT_ARGUMENTS` | imported default arguments count as custom |
| `MADEIRA_DOCK_INSTALLERS` | one-time installs are only marked done, as for the desktop client |
| `MADEIRA_DOCK_CEG` | Dock never asks the client to prepare custom executables |
| `MADEIRA_DOCK_STATUS` | the host's exit and report are not observed |
| `MADEIRA_DOCK_END_WITH_GAME` | the session stays until Quit |
| `MADEIRA_DOCK_PROGRESS` | no content download progress on the starting screen |
| `MADEIRA_DOCK_COMPACT_POOL` | the early and session pools use desktop sizing |
| `MADEIRA_DOCK_LIGHT_DIAGNOSTICS` | the D3D9 census keeps its default |
| `MADEIRA_STEAM_REGULAR_ACTIONS` | the older Windows client rows in Settings |
| `MADEIRA_DOCK_START_NOTE` | (default **off**) `=1` shows an explanatory line under the start |

Log tags: `[madeira-dock]`, `[dock-handoff]`, `[dock-report]`, `[dock-status]`,
`[dock-installers]`, `[dock-ceg]`, `[dock-session]`, `[dock-pool]`,
`[dock-heap]`, `[dock-setup]`, `[dock-arguments]`. None contains a token,
account name or path to the transfer.

## Tests

`build/host-tests/check-dock-report.py` (report parser and messages, rejection
of non-numeric and private fields), `check-dock-path.py` (the transfer path
through Wine's own resolver), `check-dock-performance.py` (pool and diagnostic
policy, desktop-reservation persistence), `check-dock-runtime.py` (exit hooks,
image-address reuse), and the Dock contract cases in `check-steam-library.py`,
`check-steam-native.py` and `check-onboarding.py` (`dock_contract.py` loads the
public contract for them).

## Status

In the 125hz fork, Dock launches reached gameplay on the owner's devices, with
real authentication and license checks by Valve's client (the host reported an
authenticated online session and the requested app in the account's licenses).
Clean-prefix native setup and broad title compatibility are less proven, and
this extraction has not been run on a device. Unknown client builds fail closed
until Dock supports them.
