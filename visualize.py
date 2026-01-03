import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def visualize_productivity(date_str):
    df = pd.read_csv('data/attendance.csv', names=["Emp ID", "Name", "Date", "Check-In", "Check-Out"])
    daily = df[df['Date'] == date_str].copy()

    def calculate_hours(row):
        try:
            in_time = datetime.strptime(str(row["Check-In"]), "%H:%M:%S")
            out_time = datetime.strptime(str(row["Check-Out"]), "%H:%M:%S")
            return (out_time - in_time).seconds / 3600
        except Exception:
            return 0

    daily["Hours Worked"] = daily.apply(calculate_hours, axis=1)
    # Drop rows where Name or Hours Worked is missing or invalid
    daily = daily.dropna(subset=["Name", "Hours Worked"])
    daily = daily[daily["Hours Worked"] > 0]
    daily["Name"] = daily["Name"].astype(str)

    plt.figure(figsize=(10, 5))
    plt.bar(daily["Name"], daily["Hours Worked"], color='skyblue')
    plt.ylabel("Hours Worked")
    plt.title(f"Productivity Chart - {date_str}")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()