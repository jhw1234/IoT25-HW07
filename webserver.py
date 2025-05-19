#!/usr/bin/env python3
from flask import Flask, jsonify, render_template_string
import serial
import threading
import time

port = "/dev/tty.usbserial-5"
baud = 115200
ser = serial.Serial(port, baud, timeout=1)

latest_line = ""

def read_serial():
    global latest_line
    while True:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                latest_line = line
            time.sleep(1)
        except Exception as e:
            latest_line = f"⚠️: {e}"

app = Flask(__name__)

html_page = """
<!DOCTYPE html>
<html>
<head>
  <title>Live Serial Monitor</title>
  <meta charset="utf-8">
  <style>
    body { font-family: sans-serif; text-align: center; margin-top: 20vh; }
    h1 { font-size: 3em; }
  </style>
</head>
<body>
  <h1 id="data">Waiting for serial data...</h1>
  <script>
    async function updateData() {
      try {
        const response = await fetch('/data');
        const text = await response.text();
        document.getElementById("data").innerText = text;
      } catch (e) {
        console.error(e);
      }
    }
    setInterval(updateData, 1000);
    updateData();
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(html_page)

@app.route("/data")
def data():
    return latest_line

threading.Thread(target=read_serial, daemon=True).start()

if __name__ == "__main__":
    print(f"Reading serial from {port} and serving on http://localhost:12345/")
    app.run(host="0.0.0.0", port=12345)
