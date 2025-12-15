#!/usr/bin/env python3

import os
import sys
import time
import subprocess
import urllib.request

SCRIPT_NAME = "kahoot-god.py"
BACKUP_NAME = "kahoot-god.old.py"

DOWNLOAD_URL = (
    "https://github.com/303entity303/kahoot-god/"
    "releases/latest/download/kahoot-god.py"
)

def fatal(msg: str):
    print(f"[UPDATER ERROR] {msg}")
    sys.exit(1)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    target_file = os.path.join(script_dir, SCRIPT_NAME)
    backup_file = os.path.join(script_dir, BACKUP_NAME)
    temp_file = target_file + ".download"

    # Give main script time to exit (Windows file lock safety)
    time.sleep(1.5)

    try:
        # Download new version
        urllib.request.urlretrieve(DOWNLOAD_URL, temp_file)
    except Exception as e:
        fatal(f"Download failed: {e}")

    try:
        # Remove old backup if it exists
        if os.path.exists(backup_file):
            os.remove(backup_file)

        # Backup current script
        if os.path.exists(target_file):
            os.rename(target_file, backup_file)

        # Replace with new script
        os.rename(temp_file, target_file)

    except PermissionError:
        # Retry once (Windows edge case)
        time.sleep(1)
        try:
            if os.path.exists(backup_file):
                os.remove(backup_file)
            if os.path.exists(target_file):
                os.rename(target_file, backup_file)
            os.rename(temp_file, target_file)
        except Exception as e:
            fatal(str(e))
    except Exception as e:
        fatal(str(e))

    # Restart updated script
    print("[UPDATER] Update successful, to restart redo the command you used to start kahoot-god.py")

if __name__ == "__main__":
    main()
