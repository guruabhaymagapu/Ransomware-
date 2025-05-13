import csv
import time
from datetime import datetime, timedelta
from collections import deque
import tkinter as tk
from tkinter import messagebox
import smtplib
from email.message import EmailMessage
import subprocess

LOG_FILE = "detection_log.csv"
THRESHOLD_EVENTS = 3
WINDOW_SECONDS = 10
SUS_EXTENSIONS = [".encrypted", ".locked", ".cry", ".pay", ".btc", ".xyz"]
DELETION_THRESHOLD = 5

def notify_admin_email(subject, body):
    sender_email = "test"
    sender_password = "password"  
    receiver_email = "test"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("Alert sent to admin.")
    except Exception as e:
        print(f"Failed to send the email: {e}")

def trigger_hardlock():
    print("Hardlock initiated: locking workstation...")
    try:
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
        print("Workstation locked successfully.")
    except Exception as e:
        print(f"Failed to lock workstation: {e}")

def user_action_gui(message):
    root = tk.Tk()
    root.withdraw()
    response = messagebox.askyesno("Suspicious Activity Detected", message)

    if not response:
        messagebox.showwarning("ALERT", "Suspicious activity noticed, Admin will be notified")
        notify_admin_email("Ransomware Alert Triggered", message)
        trigger_hardlock()
    else:
        messagebox.showinfo("Activity Approved", "Trusted changes")

def read_recent_events():
    recent_events = deque()
    now = datetime.now()
    try:
        with open(LOG_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ts = datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S")
                if (now - ts).total_seconds() <= WINDOW_SECONDS:
                    recent_events.append(row)
    except FileNotFoundError:
        print(f"No log file found at {LOG_FILE}")
    return recent_events

def analyze_recent_events(events):
    if len(events) >= THRESHOLD_EVENTS:
        user_action_gui("Multiple files changed at once, flagged as suspicious.")
        time.sleep(15)

    for e in events:
        for ext in SUS_EXTENSIONS:
            if e["File_Path"].lower().endswith(ext):
                user_action_gui(f"Found suspicious file extension:\n{e['File_Path']}")
                time.sleep(15)
                break

    deletions = [e for e in events if e["Event_Type"] == "DELETED"]
    if len(deletions) >= DELETION_THRESHOLD:
        user_action_gui(f"{len(deletions)} files deleted in {WINDOW_SECONDS} seconds.\nWas this expected?")
        time.sleep(15)

    for e in events:
        if "ransom_note.txt" in e["File_Path"].lower():
            user_action_gui("Found ransom_note.txt.\nDid you create this file?")
            time.sleep(15)
            break

def monitor_detection():
    print("Ransomware detection running")
    while True:
        recent_events = read_recent_events()
        if recent_events:
            analyze_recent_events(recent_events)
        time.sleep(5)

if __name__ == "__main__":
    monitor_detection()
