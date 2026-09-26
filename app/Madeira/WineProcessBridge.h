#pragma once
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// Start Wine process initialization on a background thread.
// Must be called AFTER wineserver is running.
// prefix_path: path to the Wine prefix directory
// Returns 0 on success, -1 on error.
int wine_process_start(const char *prefix_path);

// Check if Wine process is running
int wine_process_is_running(void);

// Session exit report (the library front end). ntdll's common exit wrapper and
// process start report each Windows program's image base name
// (server_ios.c, wine_process_did_start/wine_process_did_exit); only numeric
// state is kept here, never names.
// The last program (not a launcher/helper image) that ended with an NTSTATUS
// error in this session. Returns 1 and fills *status when there was one.
int wine_crash_exit_status(uint32_t *status);
// Forget the recorded exit status; called when a session begins.
void wine_exit_status_reset(void);
// Programs (not launcher/helper images) started / still running this session.
int wine_programs_started(void);
int wine_programs_live(void);
void wine_programs_reset(void);

// Steam S0 net-test VPN gate: write C:\madeira-continue.flag into the
// prefix's drive_c so the paused winhttp-test.exe resumes to the Steam
// stage. Called by the "Continue Net Test" UI button after the user has
// detached the JIT debugger and switched VPNs. Returns 0 on success.
int madeira_write_continue_flag(void);

#ifdef __cplusplus
}
#endif
