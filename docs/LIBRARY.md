# Library front end

Madeira starts in a game library. The original diagnostic screen (the
"developer interface") is still there: **Settings › Interface › Use developer
interface** switches to it, and its **Use New Interface** button switches back.
Either change applies at the next start (close Madeira in the app switcher and
open it again).

The code is `app/Madeira/Library.swift` and `app/Madeira/GuestDisplay.swift`
(the virtual monitor and its layout), plus the wiring in `ContentView.swift`
(`launchLibraryEntry`, `runWineFullSequence(profile:)`, `sessionBody`, the
library HUD inside `TouchControlsOverlay`, and `MetalBackedView`'s layout and
touch mapping).

## Adding games

Copy a game's whole folder into **Madeira › wine › drive_c** with the Files app,
tap **+** and choose its `.exe`. Only x86 and x64 PE executables inside drive_c
can be added; the library stores the path relative to drive_c, so a changed
app container path does not break entries. Adding an entry installs nothing.

The library reads the executable's PE imports (and those of the DLLs next to
it, plus bounded scans for dynamically loaded renderer DLL names) to show a
graphics-API badge, and measures the install folder's size. The badge names an
API only when exactly one is found: it describes what the files import, not
which renderer a game picks at run time.

Library data is written atomically to `Documents/madeira-library.json`
(version 1); covers chosen from Files are stored as thumbnails in
`Documents/madeira-art/`. A library file that cannot be read, or that has a
newer version, is left untouched and cannot be overwritten from the UI.
Removing an entry never removes the game's files or saves.

## Library screen

- Layouts: cards, compact cards, list and compact list (one short row per
  game). Sort by last played, name, date added or folder size. Search by title.
- The games section collapses by tapping its title.
- **Desktop** opens the Wine desktop (explorer and services in a virtual
  desktop) with its own profile; its Resolution is the desktop's size.
- The build label (`MadeiraBuild` in Info.plist, else the bundle version) is
  shown under the title and in the developer interface's status row.
- **Settings**: JIT and memory status, Enable JIT, extended logging, pointer
  mode (Absolute, Relative or Touch) and touch sensitivity, and the interface
  switch.

## Game details

Tapping a game opens its details page; it stays up until the session's
starting screen takes over (or an error is shown). A profile holds:

- title and cover image;
- **Resolution**: the size of the Windows screen (the virtual monitor) the game
  renders for: 640×480 to 2560×1440, plus **Screen shape**, this device's own
  aspect ratio at 720 lines (for example 1560×720 on a 19.5:9 phone), so a game
  fills the screen without bars. It is exported as the session default
  (`MADEIRA_SCREEN_W/H`, `MADEIRA_SCREEN_SRC=knob`), which win32u reports until
  the game changes the mode itself. New entries use 1280×720;
- **Aspect & scaling**: how that screen is shown. **Fit** letterboxes it,
  **Fill** covers the screen and crops, **Stretch** fills it exactly, **Aspect**
  letterboxes the shape the game actually draws (its back buffer) and **Fill
  height** keeps that shape at full height. Touches are mapped through the same
  rectangle, so input lines up in every mode;
- FPS limit: 30, 60, the display maximum or uncapped (the same presentation
  pacing modes as the FPS pill in the developer interface);
- reduced-precision x87 (`FEX_X87REDUCEDPRECISION`), fast synchronisation
  (`MADEIRA_FASTSYNC`), fast semaphore waits (`MADEIRA_FASTSYNC_SEM`, opt-in);
- **CPU cores reported**: Automatic, 1, 2, 4 or 6. Exported as
  `MADEIRA_CPU_COUNT`, which ntdll uses for the processor count Windows code
  sees; some engines size worker pools from it and misbehave with many cores;
- **D3D9 anisotropic filtering**: the application's own setting or a limit of
  1× to 8× (`DXMT_D9_ANISO_LIMIT`, read by DXMT's D3D9 front end, which is in the
  D3D9 pull request; without it the setting has no effect);
- launch arguments (double-quoted tokens, at most 64 and 4 KB in total);
- performance overlay, live logs and touch controls for the session, with the
  controls' **opacity** and overall **size**. The touch layout itself is saved
  per game from the in-game editor.

A game always starts directly. (The Steam integration adds a "Start with"
choice for Steam games.)

## Sessions

Play applies the profile and runs the same `runWineFullSequence` as the
developer interface's buttons. The game is shown full screen in either
orientation. A starting screen with the game's cover stays until the first
frames arrive (Metal presents or a desktop surface); after 30 seconds it offers
**Show game view**, and **Show live log** shows the most recent log lines.

The small menu button (drag to move; it fades after three seconds) opens the
in-game menu:

1. touch controls on/off, their **Opacity** and **Size**, **Edit controls**
   (the existing editor) and the **Keyboard** (its own key window, with an
   Esc/Ctrl/Shift/Alt/Tab/Enter/arrow row; modifiers latch);
2. the FPS limit, **Aspect & scaling**, and the mouse and pointer settings;
3. the performance overlay and its fields (FPS, average frame time, memory
   footprint, battery);
4. **Quit game** in red. Quit asks the wineserver to end the session (the
   Alt+F4 fallback is used only when that is not available).

Changes made in the menu (FPS limit, Aspect & scaling, controls, overlay) are
saved to the game's profile.

**Pointer modes.** Absolute drags the pointer like a trackpad, Relative sends
finger movement as mouse movement (mouse-look), and **Touch** clicks where the
finger is: tap to click, hold or move to drag, a two- or three-finger tap for a
right or middle click, a two-finger drag to scroll. Touch works in direct and
desktop sessions.

When the session ends Madeira returns to the library, restores the touch layout
it had before, and hides the ended session's surfaces. If the session ended by
itself, a message says why when that is known: an earlier session ran the JIT
pool dry (the next start reserves more), or the game exited with a Windows
error status (for example `0xC0000005`, memory access violation). The status
comes from ntdll's process start/exit hooks (`wine_process_did_start` /
`wine_process_did_exit` in `build/ntdll-unix/server_ios.c`), which report only
the image's base name; the app keeps counters and the last error status, never
names. Launcher and helper images (explorer, services, cmd, ...) are not counted.

One Wine session runs per app run: a second one cannot start in the same
process (the wineserver's permanent objects from the first session remain and
the registry initialisation aborts). The library asks to restart Madeira
instead.

## Controllers

Player 1's controller navigates the library through `GamepadInput`: D-pad or
left stick moves the focus, A opens and plays, B goes back, Y adds a game and
the shoulder buttons switch between Library and Settings. In a session,
Back+Start opens the in-game menu and B closes it. While the library or its
menu owns input, the game sees a connected pad at rest.

## Switches

`env.NAME = 0` in `Documents/madeira.cfg` (or `NAME=0` in `madeira-env.txt`):

| Switch | Default | `0` means |
| --- | --- | --- |
| `MADEIRA_FRONTEND_DEFAULT_NEW` | on | the developer interface is the default |
| `MADEIRA_FRONTEND` | unset | `env.MADEIRA_FRONTEND = 0/1` picks the interface when nothing was chosen in the app |
| `MADEIRA_FRONTEND_CONTROLLER` | on | no controller navigation |
| `MADEIRA_ONE_SESSION_PER_RUN` | on | a second session is attempted anyway |
| `MADEIRA_EXIT_REPORT` | on | no message when a session ends by itself |
| `MADEIRA_JIT_RECONNECT` | on | Play asks to enable JIT instead of reopening StikDebug |
| `MADEIRA_LIBRARY_HIDE_ENDED_DESKTOP` | on | the ended desktop's surface is left as it was |
| `MADEIRA_BUILD_LABEL` | on | no build label (the `[build]` log line stays) |
| `MADEIRA_UI_LOG_IDLE` | on | the log view keeps parsing while hidden |
| `MADEIRA_LOG_VIA_STDERR` | on | Swift log lines use their own file handle |
| `MADEIRA_DEVICE_STATS` | on | no `[device-load]` line |
| `MADEIRA_PROMOTE` | on | the display link is armed only outside the 60 FPS cap |
| `MADEIRA_SESSION_TOOLS` | on | no Aspect & scaling in the in-game menu, and a session does not save it |
| `MADEIRA_SCREEN_SHAPE_RESOLUTION` | on | no Screen shape resolution choice |
| `MADEIRA_FRONTEND_KEYBOARD` | on | Keyboard opens the game view's own keyboard instead of the key window |

Log tags: `[frontend]`, `[display]`, `[display-shape]`, `[frontend-pointer]`, `[launch-view]`, `[startup-log]`, `[exit-report]`,
`[session-once]`, `[library-surface]`, `[library-metadata]`,
`[frontend-controller]`, `[frontend-keyboard]`, `[device-load]`, `[promote]`.

## Tests

`build/host-tests/check-frontend.py` (profiles incl. resolution, scaling and
anisotropy, the display layout math, controller commands, exit hooks, and the
presence of the details and in-game menu options)
and `build/host-tests/check-library-api.py` (renderer detection and the badge).
