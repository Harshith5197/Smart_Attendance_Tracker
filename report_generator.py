import pandas as pd
from datetime import datetime

def generate_daily_report(date_str):
    df = pd.read_csv('data/attendance.csv', names=["Emp ID", "Name", "Date", "Check-In", "Check-Out"])
    daily = df[df['Date'] == date_str]

    print(f"\n📅 Report for {date_str}")
    print(daily[["Emp ID", "Name", "Check-In", "Check-Out"]])

    daily.to_csv(f'reports/{date_str}_report.csv', index=False)