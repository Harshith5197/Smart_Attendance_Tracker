import csv
from datetime import datetime

FILENAME = 'data/attendance.csv'

def check_in(emp_id, name):
    now = datetime.now()
    with open(FILENAME, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([emp_id, name, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), ""])

    print(f"[✓] Check-in recorded for {name} at {now.strftime('%H:%M:%S')}")

def check_out(emp_id):
    lines = []
    updated = False

    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == emp_id and row[4] == "":
                row[4] = datetime.now().strftime("%H:%M:%S")
                updated = True
            lines.append(row)

    with open(FILENAME, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(lines)

    if updated:
        print("[✓] Check-out successful.")
    else:
        print("[!] No pending check-in found.")