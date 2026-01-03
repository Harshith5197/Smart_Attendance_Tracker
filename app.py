from flask import Flask, request, jsonify
import checkin_checkout
import report_generator
import visualize
import pandas as pd
import os

app = Flask(__name__)

DATA_FILE = 'data/attendance.csv'

@app.route("/")
def home():
    return "Smart Attendance System API is running."

@app.route("/checkin", methods=["POST"])
def checkin():
    data = request.get_json()
    emp_id = data.get("emp_id")
    name = data.get("name")
    result = checkin_checkout.check_in(emp_id, name)
    return jsonify({"message": f"Check-in recorded for {name}."})

@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.get_json()
    emp_id = data.get("emp_id")
    result = checkin_checkout.check_out(emp_id)
    return jsonify({"message": "Check-out successful." if result else "No pending check-in found."})

@app.route("/attendance", methods=["GET"])
def get_attendance():
    if not os.path.exists(DATA_FILE):
        return jsonify({"error": "Attendance file not found."}), 404
    df = pd.read_csv(DATA_FILE, names=["Emp ID", "Name", "Date", "Check-In", "Check-Out"])
    records = df.to_dict(orient="records")
    return jsonify(records)

@app.route("/report", methods=["GET"])
def report():
    date_str = request.args.get("date")  # e.g., /report?date=2025-08-07
    if not date_str:
        return jsonify({"error": "Missing 'date' parameter"}), 400
    report_path = report_generator.generate_daily_report(date_str)
    return jsonify({"report_path": report_path})

@app.route("/visualize", methods=["GET"])
def visualize_attendance():
    date_str = request.args.get("date")  # e.g., /visualize?date=2025-08-07
    if not date_str:
        return jsonify({"error": "Missing 'date' parameter"}), 400
    visualize.visualize_productivity(date_str)
    return jsonify({"message": f"Attendance visualized for {date_str}"})

if __name__ == "__main__":
    app.run(debug=True)
