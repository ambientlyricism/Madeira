# Steam account, library and downloads

This adds Steam to the library front end (`docs/LIBRARY.md`): sign-in to the
user's own Steam account, the account's Windows games in the library with
playtime and artwork, downloads straight from Steam's content servers, and the
regular Windows Steam client running inside Madeira for games that need Steam
running.

Steam itself authenticates the account and decides ownership: depot keys are
only issued for depots the signed-in account owns, and games are downloaded
unmodified into a normal Steam library folder in drive_c. **Nothing here
emulates Steam, unwraps or patches DRM, injects tickets or loads games through
a replacement `steam_api`.** A game that needs Steam running is started by the
genuine Windows Steam client.

## Code and credit

- `app/Madeira/SwiftSteam/`: the Steam protocol (connection-manager WebSocket,
  protobuf messages, crypto), sign-in (QR and password with Steam Guard),
  owned-library and app-info (PICS) fetching, depot manifests, chunk
  decryption and decompression (VZstd, VZip/LZMA, PKZip), and the depot
  downloader. **Derived from Jfishin's Madeira Steam client** in
  [Jfishin/Madeira-source](https://github.com/Jfishin/Madeira-source), a
  GPL-3.0-or-later fork of this repository (commit `c9cfb74`). Each derived
  file carries an attribution header. That tree's Steam Cloud, launch
  emulator, ticket and DRM-related components are not included. The download
  orchestration, the password and Steam Guard flow and logging were rewritten;
  the zip-chunk decoder and the shared sign-in transport are new.
- `SwiftSteam/zstd_edu.c/.h`: the Zstandard educational decoder (Meta
  Platforms, BSD-3-Clause; `LICENSES/ZSTD-BSD.txt`), with its error recovery
  serialized across threads. LZMA chunks use the iOS system liblzma.
- `SteamAccount.swift` (account, library, downloads, background downloads,
  playtime), `SteamStoreViews.swift` (sign-in, owned games, per-game Steam
  options, license agreements), `SteamLibrary.swift` (the Windows client:
  install, open, scan), `SteamFiles.swift` (KeyValues reader, paths, launch
  scene, license agreements, one-time installs), `SteamInstallRegistry.swift`,
  `Onboarding.swift` (first-run setup), and the Steam parts of
  `Library.swift`/`ContentView.swift`.

## Sign in

Settings › Steam, the library's Steam section, or first-run setup.

- **Password**: the Steam *account name* and password, then a Steam Guard code
  (Steam app or email) or approval in the Steam app; both are offered when
  Steam allows both. The password is RSA-encrypted with Steam's key before it
  leaves the device and is never stored. Typed-password sign-in sends the
  fields Steam's authentication service expects (field numbers fixed against
  the service definition).
- **QR code** (default on iPad): scan it with the Steam app on another device.

The refresh token is kept in the iOS Keychain (this device only) until
**Sign out**. An expired or revoked token signs the app out with a message.
No log line contains an account name, token or password.

## Library

The library gets a **Steam** section (installed and downloading games, and a
collapsible **Not installed** list of every owned game with a Windows build)
and **Other games** (everything added by hand). Owned games come from the
account's licenses and app info; demos, tools and non-Windows apps are left
out. Playtime and last played come from the account's own
`Player.GetOwnedGames` over the same connection. Artwork is the store's
library capsule and hero from app info, with fallbacks to the legacy CDN path,
a demo's full game and the store's header image (public store endpoints, no
account data). Games added by hand get artwork from Steam's public store search
(nearest title; **Find on Steam** to pick another, or a cover from Files).

## Downloads

**Install** on a game downloads it into
`C:\Program Files (x86)\Steam\steamapps\common\<folder>` and writes the normal
`appmanifest_<appid>.acf`, so the Windows client recognizes it.

- Windows depots only: common and English content, 64-bit (or 32-bit when that
  is all there is); DLC, low-violence alternates and shared redistributables
  are skipped. A depot Steam refuses a key for and the account's licenses do
  not include (another edition, extra content) is left out, as Valve's
  DepotDownloader does; any other refusal fails the download.
- Shared depots: content another app owns is fetched with that owner's
  metadata, and the owner gets its own install record, as the client does.
- Custom executables: files Steam marks as per-user custom executables are
  listed in the record's `CheckGuid` block and their manifests kept in
  `steamapps/depotcache`, the records Valve's client reads when it prepares
  such an executable for the user itself. Madeira never alters them.
- Completed chunks are journaled in `steamapps/downloading/<appid>`, so a
  download resumes where it stopped; existing files are checked chunk by chunk
  (SHA-1), so updates fetch only changed data. **Repair installed files**
  re-checks an install against the current build.
- Content servers without HTTPS, proxy-only and app-restricted servers are
  skipped; a failing server moves to the back of the rotation.
- Downloads pause while a game runs and continue afterwards.
- **Background:** on iOS 26 and later a `BGContinuedProcessingTask` keeps the
  queue going when Madeira leaves the foreground, with the system's own
  progress UI. On earlier versions, or when iOS refuses the request, the short
  background grace period applies, then the download pauses cleanly and
  resumes when Madeira is opened again. A notification reports a finished,
  failed or paused download while Madeira is in the background. The task
  identifier comes from `BGTaskSchedulerPermittedIdentifiers` in Info.plist
  (`$(PRODUCT_BUNDLE_IDENTIFIER).download.*`, expanded by Xcode).

The program to start comes from Steam's launch entries (default type, 64-bit or
neutral first) or, failing that, the most likely executable in the folder;
redistributables and installers are never chosen.

## Starting a Steam game

Game details › Steam › **Start with**:

- **The game** runs the executable directly. A `steam_appid.txt` (Valve's
  documented developer file) is written next to it, and the launch publishes
  `SteamAppPath` (the executable's folder) and the app ID (WineProcessBridge,
  `[steam-env]`). This works for games that do not need Steam running.
- **Steam client** runs the Windows Steam client with `-applaunch <appid>` in
  the virtual desktop. It needs the client installed and signed in to the same
  account. Without a stored choice this is the default once the client is
  installed.

For a client start, before Wine starts:

- license agreements listed in the app's info and not yet accepted are shown in
  Madeira; accepting records them in the client's `localconfig.vdf` exactly as
  the client does (a backup is kept);
- the game's one-time installs (DirectX, Visual C++ and similar, which Wine
  provides) are marked done in the prefix registry unless "Run Steam's one-time
  installs" is on, and the install script's registry values are written;
- Madeira's own Steam connection logs off, so the two sign-ins do not replace
  each other.

While the client works, a starting screen covers the Wine desktop until a
window of the started game is up (decided from Winios's per-window census by
owning program, `SteamLaunchScene`). It shows the client's stage and download
progress from the client's own logs and install records. A client window that
needs the user (sign-in, an error, an installer's dialog) is revealed, and
**Show Steam** reveals the desktop on request; **Skip one-time installs** ends
a session stuck in them and asks for a restart.

The client runs lighter: no overlay, friends UI, shader pre-cache, crash
reporter or Big Picture during a game launch (`-silent` keeps its library
window closed). Its helper programs get consoles without windows (kernelbase,
companion Wine change), lower iOS scheduling classes, and its web helper is
held at its next wait from 10 s after the game's window appears until the
session ends, with a watchdog that releases it if the game stops presenting
(ntdll `[thread-qos]`/`[park]`, companion Wine change).

## The Windows Steam client

Settings › Steam › **Windows Steam client…** downloads Valve's `SteamSetup.exe`
from Steam's CDN (HTTPS, Valve hosts only, at most 32 MB) or takes one from
Files, and runs it in the Wine desktop; **Open Steam** and **Big Picture** open
the installed client. An existing installation elsewhere in drive_c can be
chosen. The client's installed games are imported into the library. Installer
sessions keep `services.exe` running after the installer so the client it
starts survives. A Steam folder made by Madeira's downloader is moved aside
while the installer runs (it refuses a non-empty folder) and merged back after.

**First-run setup** (new installs): install the Windows client, sign in, done.
The setup's session gets the largest JIT pool, and Madeira asks for a restart
before the first game (one Wine session per app run).

## Switches

`env.NAME = 0` in `Documents/madeira.cfg` (or `NAME=0` in `madeira-env.txt`).
All default on unless noted.

| Switch | `0` means |
| --- | --- |
| `MADEIRA_STEAM` | no Steam at all |
| `MADEIRA_STEAM_NATIVE` | no sign-in, owned library or downloads (the Windows client stays) |
| `MADEIRA_LIBRARY_SECTIONS` | one combined grid instead of Steam / Other games |
| `MADEIRA_ONBOARDING` | first-run setup never opens |
| `MADEIRA_STEAM_DEFAULT_CLIENT` | "The game" is the default start mode |
| `MADEIRA_STEAM_REQUIRE_CLIENT` | Install does not ask for the Windows client first |
| `MADEIRA_STEAM_PAUSE_FOR_SESSION` | downloads continue while a game runs |
| `MADEIRA_BACKGROUND_DOWNLOADS` | downloads stop with the app, as before |
| `MADEIRA_DOWNLOAD_NOTIFICATIONS` | no download notifications |
| `MADEIRA_STEAM_PLAYTIME` | no playtime or last played |
| `MADEIRA_STEAM_ARTWORK` | one legacy artwork URL only |
| `MADEIRA_STEAM_CATALOG` | no automatic store-search artwork for games added by hand |
| `MADEIRA_STEAM_APPID_FILE` | no `steam_appid.txt` next to installed executables |
| `MADEIRA_STEAM_ENV` | no Steam identity published for direct launches |
| `MADEIRA_STEAM_SHARED_METADATA`, `MADEIRA_STEAM_SHARED_RECORDS`, `MADEIRA_STEAM_CEG_RECORDS`, `MADEIRA_STEAM_LICENSE_DEPOTS` | the corresponding download record or rule is left out |
| `MADEIRA_STEAM_EULA_NATIVE` | license agreements are left to the client |
| `MADEIRA_STEAM_SKIP_INSTALLERS`, `MADEIRA_STEAM_INSTALL_REGISTRY` | one-time installs / install-script registry values are left to the client |
| `MADEIRA_STEAM_HIDE_DESKTOP`, `MADEIRA_STEAM_AUTO_REVEAL` | no starting screen over the client / no automatic reveal |
| `MADEIRA_STEAM_SILENT`, `MADEIRA_STEAM_LIGHT`, `MADEIRA_STEAM_CEF_LIGHT`, `MADEIRA_STEAM_COMPAT` | the corresponding client command-line options are omitted |
| `MADEIRA_STEAM_HEADLESS_CONSOLES` | the client's console windows are shown |
| `MADEIRA_STEAM_BACKGROUND_QOS`, `MADEIRA_STEAM_HELPER_BACKGROUND` | every client thread stays interactive |
| `MADEIRA_STEAM_WEBHELPER_FREEZE`, `MADEIRA_STEAM_FREEZE_WATCHDOG` | the web helper keeps running / is never released |
| `MADEIRA_STEAM_INSTALL_KEEPALIVE`, `MADEIRA_STEAM_INSTALL_MOVE_ASIDE` | installer session without services.exe / folder left in place |
| `MADEIRA_POOL_SETUP_896` | setup's session gets the normal pool |
| `MADEIRA_LIBRARY_STEAM_BUTTON` | (default **off**) `=1` shows a Steam button in the library |
| `MADEIRA_STEAM_TRACE` | (default **off**) `=1` protocol-level `[steam-trace]` lines, no credentials or payloads |

Log tags (no account names, tokens or game titles): `[steam-account]`,
`[steam-library]`, `[steam-depot]`, `[steam-cdn]`, `[steam-play]`,
`[steam-playtime]`, `[bg-download]`, `[steam-launch-view]`, `[steam-progress]`,
`[steam-stage]`, `[steam-eula]`, `[steam-installers]`, `[steam-registry]`,
`[steam-env]`, `[onboarding]`, `[setup-stage]`, `[park]`.

## Tests

`build/host-tests/check-steam-native.py` (depot selection, manifest path
safety, the download journal, appmanifest output, launch routing; the C
decoders under ASan and TSan), `check-steam-library.py` (KeyValues, paths,
installers, staging, one-time installs), `check-steam-launch-view.py` (launch
scene, hold, Workshop progress, the Winios census), `check-onboarding.py`,
`check-steam-env.py`, and, for the companion Wine change,
`check-console-headless.py` and `check-steam-connlog.py`.
