#!/usr/bin/env python3
"""
Seamless KC-Riff Runner
This script automatically starts both the Go server and the PyQt interface
for a completely seamless user experience.
"""

import os
import sys
import subprocess
import threading
import time
import signal
import atexit

# Try to import PyQt5, install if not available
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
    from PyQt5.QtCore import Qt, QTimer
except ImportError:
    print("PyQt5 not found. Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
    from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
    from PyQt5.QtCore import Qt, QTimer

try:
    import requests
except ImportError:
    print("Requests not found. Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# Global variables
server_process = None

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
        
        self.status = QLabel("Starting server...")
        layout.addWidget(self.status)
        
        # Buttons
        self.list_button = QPushButton("List Models")
        self.list_button.clicked.connect(self.list_models)
        layout.addWidget(self.list_button)
        
        self.download_button = QPushButton("Download Recommended Models")
        self.download_button.clicked.connect(self.download_recommended)
        layout.addWidget(self.download_button)
        
        # Set up a timer to repeatedly check server status
        self.server_timer = QTimer()
        self.server_timer.timeout.connect(self.check_server)
        self.server_timer.start(1000)  # Check every second
        
        # Track server connection status
        self.server_connected = False
    
    def check_server(self):
        try:
            response = requests.get("http://localhost:5000/api/health")
            response.raise_for_status()
            
            if not self.server_connected:
                self.status.setText("Server started and running!")
                self.status.setStyleSheet("color: green;")
                self.server_connected = True
                
                # Stop checking once connected
                self.server_timer.stop()
        except Exception:
            self.status.setText("Server starting... please wait")
    
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

    def closeEvent(self, event):
        """Handle window close event by stopping the server"""
        stop_server()
        event.accept()

def start_server():
    """Start the Go backend server in a separate process"""
    global server_process
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        server_path = os.path.join(script_dir, "minimal_server.go")
        
        if not os.path.exists(server_path):
            print(f"Warning: Server file not found at {server_path}")
            return False
        
        print("Starting KC-Riff server...")
        server_process = subprocess.Popen(
            ["go", "run", server_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Monitor stdout and stderr
        def monitor_output(stream, prefix):
            for line in stream:
                print(f"{prefix}: {line.strip()}")
        
        threading.Thread(target=monitor_output, args=(server_process.stdout, "SERVER"), daemon=True).start()
        threading.Thread(target=monitor_output, args=(server_process.stderr, "SERVER ERROR"), daemon=True).start()
        
        print("Server process started")
        return True
    except Exception as e:
        print(f"Failed to start Go backend: {e}")
        return False

def stop_server():
    """Stop the server process when the application exits"""
    global server_process
    if server_process:
        print("Stopping KC-Riff server...")
        try:
            if sys.platform == 'win32':
                # Windows
                server_process.terminate()
            else:
                # Unix-like
                server_process.send_signal(signal.SIGTERM)
            
            # Wait for process to terminate
            server_process.wait(timeout=5)
            print("Server stopped")
        except Exception as e:
            print(f"Error stopping server: {e}")
            # Force kill if necessary
            server_process.kill()

def is_server_running():
    """Check if the server is already running"""
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=1)
        return response.status_code == 200
    except:
        return False

def main():
    """Main function"""
    # Register cleanup function
    atexit.register(stop_server)
    
    # Check if server is already running
    server_running = is_server_running()
    if not server_running:
        # Start the server
        if not start_server():
            print("Failed to start server, exiting")
            return
    else:
        print("Server is already running")
    
    # Start PyQt application
    app = QApplication(sys.argv)
    window = SimpleKCRiffDesktop()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()