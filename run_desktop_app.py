#!/usr/bin/env python3
"""
Runner script for KC-Riff desktop application.
This script starts the PyQt5-based desktop interface that connects to our minimal server.
"""

import os
import sys
import subprocess
import threading
import time

# Try to import PyQt5, install if not available
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
except ImportError:
    print("PyQt5 not found. Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
    from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget

try:
    import requests
except ImportError:
    print("Requests not found. Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

class SimpleKCRiffDesktop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KC-Riff Desktop")
        self.setGeometry(100, 100, 600, 400)
        
        # Central widget and layout
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Labels
        self.title = QLabel("KC-Riff Model Manager")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(self.title)
        
        self.status = QLabel("Checking server status...")
        layout.addWidget(self.status)
        
        # Buttons
        self.list_button = QPushButton("List Models")
        self.list_button.clicked.connect(self.list_models)
        layout.addWidget(self.list_button)
        
        self.download_button = QPushButton("Download Recommended Models")
        self.download_button.clicked.connect(self.download_recommended)
        layout.addWidget(self.download_button)
        
        # Check server status
        self.check_server()
    
    def check_server(self):
        try:
            response = requests.get("http://localhost:5000/api/health")
            response.raise_for_status()
            self.status.setText("Server is running!")
            self.status.setStyleSheet("color: green;")
        except Exception as e:
            self.status.setText(f"Server error: {str(e)}")
            self.status.setStyleSheet("color: red;")
    
    def list_models(self):
        try:
            response = requests.get("http://localhost:5000/api/models")
            response.raise_for_status()
            models = response.json()
            
            model_text = "Available Models:\n\n"
            for model in models:
                status = "Downloaded" if model.get("downloaded", False) else "Not Downloaded"
                recommended = " [RECOMMENDED]" if model.get("kc_recommended", False) else ""
                model_text += f"- {model['name']}{recommended}: {status}\n"
            
            self.status.setText(model_text)
            self.status.setStyleSheet("font-family: monospace;")
        except Exception as e:
            self.status.setText(f"Error listing models: {str(e)}")
            self.status.setStyleSheet("color: red;")
    
    def download_recommended(self):
        try:
            response = requests.get("http://localhost:5000/api/models")
            response.raise_for_status()
            models = response.json()
            
            recommended = [model["name"] for model in models if model.get("kc_recommended", False)]
            
            if not recommended:
                self.status.setText("No recommended models found.")
                return
            
            self.status.setText(f"Downloading recommended models: {', '.join(recommended)}")
            
            # Start downloads
            for model_name in recommended:
                requests.get(f"http://localhost:5000/api/models/download?name={model_name}")
            
            self.status.setText("Downloads started in background. Check server logs for progress.")
        except Exception as e:
            self.status.setText(f"Error downloading models: {str(e)}")
            self.status.setStyleSheet("color: red;")

def start_go_backend():
    """Start the Go backend server in a separate process"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        server_path = os.path.join(script_dir, "minimal_server.go")
        
        if not os.path.exists(server_path):
            print(f"Warning: Server file not found at {server_path}")
            return None
        
        process = subprocess.Popen(
            ["go", "run", server_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Monitor stderr for errors
        def monitor_stderr():
            for line in process.stderr:
                print(f"SERVER ERROR: {line.strip()}")
        
        threading.Thread(target=monitor_stderr, daemon=True).start()
        
        # Wait for server to start
        time.sleep(2)
        return process
    except Exception as e:
        print(f"Failed to start Go backend: {e}")
        return None

def main():
    """Main function"""
    # Start backend if not already running
    try:
        # Check if server is already running
        requests.get("http://localhost:5000/api/health")
        print("Server is already running")
    except:
        print("Starting server...")
        server_process = start_go_backend()
    
    # Start PyQt application
    app = QApplication(sys.argv)
    window = SimpleKCRiffDesktop()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()