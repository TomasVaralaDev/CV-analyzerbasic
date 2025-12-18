import subprocess

# Käynnistää Flask-backendin ja GUI:n rinnakkain
subprocess.Popen(["python", "backend/app.py"])
subprocess.call(["python", "frontend/gui.py"])
