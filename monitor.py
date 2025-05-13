import time
import csv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from datetime import datetime



WATCH_DIR = "critical"


if not os.path.exists("detection_log.csv"):
    with open("detection_log.csv", mode='w', newline='') as log:
        writer = csv.writer(log)
        writer.writerow(["Timestamp", "Event_Type", "File_Path"])

#we create three functions to handle three actions i.e modify, create and delete
class MonitorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        self.log_event("MODIFIED", event.src_path)

    def on_created(self, event):
        self.log_event("CREATED", event.src_path)

    def on_deleted(self, event):
        self.log_event("DELETED", event.src_path)

    def log_event(self, event_type, path):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open("detection_log.csv", mode='a', newline='') as log:
            writer = csv.writer(log)
            writer.writerow([timestamp, event_type, path])
        print(f"[{timestamp}] {event_type} - {path}")

if __name__ == "__main__":
    if not os.path.exists(WATCH_DIR):
        print(f"Directory '{WATCH_DIR}' not found.")
        exit()

    print(f"Monitoring the sensitive folder: {WATCH_DIR}")
    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("stopping monitor script")
    observer.join()
