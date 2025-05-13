import os
import shutil
import time
import datetime

SOURCE_DIR = "critical"
BACKUP_DIR = "backups"
INTERVAL_SECONDS = 1800  

def create_backup():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = os.path.join(BACKUP_DIR, f"backup_{timestamp}")
    try:
        shutil.copytree(SOURCE_DIR, destination)
        print(f"[{timestamp}] Backup created at: {destination}")
    except Exception as e:
        print(f"Backup failed: {e}")

def ensure_directories():
    if not os.path.exists(SOURCE_DIR):
        print(f"Source folder '{SOURCE_DIR}' does not exist.")
        exit()
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

if __name__ == "__main__":
    ensure_directories()
    print(f"Starting periodic backup every {INTERVAL_SECONDS // 60} minutes...")

    while True:
        create_backup()
        time.sleep(INTERVAL_SECONDS)
