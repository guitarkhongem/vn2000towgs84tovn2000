import subprocess
import sys
import os
import time
import webbrowser

def resource_path(path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, path)
    return os.path.abspath(path)

app_path = resource_path("app.py")

subprocess.Popen([
    sys.executable,
    "-m", "streamlit", "run", app_path,
    "--server.headless=true",
    "--server.port=8501"
])

time.sleep(3)
webbrowser.open("http://localhost:8501")
