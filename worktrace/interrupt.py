"""Clean Ctrl+C for long runs: the first press stops starting new work and lets runs in progress finish and be saved;
a second press quits at once. The process then exits with code 130, so shell scripts with `set -e` stop as well."""
from __future__ import annotations

import os
import signal
import threading

STOP = threading.Event()


def _handler(signum, frame) -> None:
    if STOP.is_set():
        print("\nStopped at once. Runs in progress were not saved; re-run the same command to continue.", flush=True)
        os._exit(130)
    STOP.set()
    print("\nStopping: finishing the runs in progress (Ctrl+C again to quit at once). "
          "Re-run the same command to continue.", flush=True)


def install() -> None:
    signal.signal(signal.SIGINT, _handler)
