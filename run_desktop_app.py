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
    from PyQt5.QtWidgets import QApplication
except ImportError:
    print("PyQt5 not found. Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
    from PyQt5.QtWidgets import QApplication

try:
    import requests
except ImportError:
    print("Requests not found. Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# Add script directory to path so we can import from pyqt_interface
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

# Create pyqt_interface directory if it doesn't exist
pyqt_interface_dir = os.path.join(script_dir, "pyqt_interface")
os.makedirs(pyqt_interface_dir, exist_ok=True)

# Create kcriff_desktop.py if it doesn't exist
desktop_py_path = os.path.join(pyqt_interface_dir, "kcriff_desktop.py")
if not os.path.exists(desktop_py_path):
    print("Creating desktop interface script...")
    
    with open(desktop_py_path, "w") as f:
        f.write("""#!/usr/bin/env python3
\"\"\"
KC-Riff Desktop Application
A PyQt-based desktop interface for KC-Riff, the enhanced Ollama fork.
\"\"\"

import os
import sys
import json
import time
import threading
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QGridLayout, QProgressBar,
    QScrollArea, QSplitter, QSizePolicy, QTabWidget, QMessageBox
)
from PyQt5.QtCore import (
    Qt, QThread, pyqtSignal, QSize, QTimer, QUrl, QRect
)
from PyQt5.QtGui import (
    QColor, QPalette, QFont, QPixmap, QImage, QIcon
)

# Default server URL
DEFAULT_SERVER_URL = "http://localhost:5000"

class ModelDownloadThread(QThread):
    \"\"\"Thread to download models without blocking the UI\"\"\"
    progress_updated = pyqtSignal(str, float)
    download_complete = pyqtSignal(str, bool)

    def __init__(self, model_name):
        super().__init__()
        self.model_name = model_name
        self.running = True

    def run(self):
        \"\"\"Download a model and emit progress updates\"\"\"
        try:
            # Start the download
            response = requests.get(f"{DEFAULT_SERVER_URL}/api/models/download?name={self.model_name}")
            response.raise_for_status()
            
            # Poll for status updates
            while self.running:
                status_response = requests.get(f"{DEFAULT_SERVER_URL}/api/models/status?name={self.model_name}")
                status_response.raise_for_status()
                status = status_response.json()
                
                progress = float(status.get("progress", 0))
                self.progress_updated.emit(self.model_name, progress)
                
                if status.get("completed", False):
                    success = status.get("status") == "completed"
                    self.download_complete.emit(self.model_name, success)
                    break
                
                time.sleep(0.5)
        except Exception as e:
            print(f"Error in download thread: {e}")
            self.download_complete.emit(self.model_name, False)

    def stop(self):
        \"\"\"Request the thread to stop\"\"\"
        self.running = False


class BatchDownloadThread(QThread):
    \"\"\"Thread to download multiple models\"\"\"
    progress_updated = pyqtSignal(dict)  # {model_name: progress}
    batch_complete = pyqtSignal(bool, str)

    def __init__(self, model_names=None, download_recommended=False):
        super().__init__()
        self.model_names = model_names or []
        self.download_recommended = download_recommended
        self.running = True

    def run(self):
        \"\"\"Download all models in the batch\"\"\"
        try:
            # If downloading recommended models, get the list first
            if self.download_recommended and not self.model_names:
                response = requests.get(f"{DEFAULT_SERVER_URL}/api/models")
                response.raise_for_status()
                models = response.json()
                self.model_names = [m["name"] for m in models if m.get("kc_recommended", False)]
            
            if not self.model_names:
                self.batch_complete.emit(False, "No models selected for download")
                return
            
            # Start all downloads
            downloads = {}
            for name in self.model_names:
                response = requests.get(f"{DEFAULT_SERVER_URL}/api/models/download?name={name}")
                response.raise_for_status()
                downloads[name] = 0
            
            # Poll for status updates
            all_complete = False
            while self.running and not all_complete:
                progress_dict = {}
                all_complete = True
                
                for name in self.model_names:
                    status_response = requests.get(f"{DEFAULT_SERVER_URL}/api/models/status?name={name}")
                    status_response.raise_for_status()
                    status = status_response.json()
                    
                    progress = float(status.get("progress", 0))
                    progress_dict[name] = progress
                    
                    if not status.get("completed", False):
                        all_complete = False
                
                self.progress_updated.emit(progress_dict)
                
                if all_complete:
                    self.batch_complete.emit(True, "All models downloaded successfully")
                    break
                
                time.sleep(0.5)
                
        except Exception as e:
            print(f"Error in batch download thread: {e}")
            self.batch_complete.emit(False, str(e))

    def stop(self):
        \"\"\"Request the thread to stop\"\"\"
        self.running = False


class ModelCard(QFrame):
    \"\"\"Custom widget for displaying a model with download/remove buttons\"\"\"
    
    def __init__(self, model_data, parent=None, dark_mode=True):
        super().__init__(parent)
        self.model_data = model_data
        self.download_thread = None
        self.dark_mode = dark_mode
        
        # Card style
        self.setFrameShape(QFrame.StyledPanel)
        self.setLineWidth(1)
        self.setMinimumHeight(150)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.setup_ui()
        self.update_state()
        
    def setup_ui(self):
        \"\"\"Create the UI components\"\"\"
        layout = QVBoxLayout(self)
        
        # Model name
        self.name_label = QLabel(self.model_data.get("name", "Unknown"))
        name_font = QFont()
        name_font.setPointSize(12)
        name_font.setBold(True)
        self.name_label.setFont(name_font)
        
        # Description
        self.desc_label = QLabel(self.model_data.get("description", "No description available"))
        self.desc_label.setWordWrap(True)
        
        # Size and parameters
        size_mb = self.model_data.get("size", 0) / 1000000
        params_b = self.model_data.get("parameters", 0) / 1000000000
        self.info_label = QLabel(f"Size: {size_mb:.0f}MB | Parameters: {params_b:.1f}B")
        
        # Recommended badge
        self.rec_label = QLabel("✓ Recommended for KillChaos")
        rec_font = QFont()
        rec_font.setPointSize(10)
        rec_font.setBold(True)
        self.rec_label.setFont(rec_font)
        self.rec_label.setVisible(self.model_data.get("kc_recommended", False))
        
        # Progress bar for downloads
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        
        # Action button (Download or Remove)
        self.action_button = QPushButton("Download")
        self.action_button.clicked.connect(self.on_action_button_clicked)
        
        # Add to layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.desc_label)
        layout.addWidget(self.info_label)
        layout.addWidget(self.rec_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.action_button)
        
        # Apply colors based on mode
        if self.dark_mode:
            recommended_color = QColor(0, 180, 0)
            self.rec_label.setStyleSheet(f"color: rgb({recommended_color.red()}, {recommended_color.green()}, {recommended_color.blue()})")
        else:
            recommended_color = QColor(0, 120, 0)
            self.rec_label.setStyleSheet(f"color: rgb({recommended_color.red()}, {recommended_color.green()}, {recommended_color.blue()})")
    
    def update_state(self):
        \"\"\"Update the UI based on model state\"\"\"
        if self.model_data.get("downloaded", False):
            self.action_button.setText("Remove")
            self.progress_bar.setVisible(False)
        else:
            self.action_button.setText("Download")
            # Show progress bar if download is in progress
            self.progress_bar.setVisible(False)
    
    def update_model_data(self, model_data):
        \"\"\"Update with new model data\"\"\"
        self.model_data = model_data
        self.name_label.setText(model_data.get("name", "Unknown"))
        self.desc_label.setText(model_data.get("description", "No description available"))
        
        size_mb = model_data.get("size", 0) / 1000000
        params_b = model_data.get("parameters", 0) / 1000000000
        self.info_label.setText(f"Size: {size_mb:.0f}MB | Parameters: {params_b:.1f}B")
        
        self.rec_label.setVisible(model_data.get("kc_recommended", False))
        self.update_state()
    
    def on_action_button_clicked(self):
        \"\"\"Handle download or remove button click\"\"\"
        if self.model_data.get("downloaded", False):
            self.remove_model()
        else:
            self.download_model()
    
    def download_model(self):
        \"\"\"Start downloading the model\"\"\"
        self.action_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        
        self.download_thread = ModelDownloadThread(self.model_data["name"])
        self.download_thread.progress_updated.connect(self.update_progress)
        self.download_thread.download_complete.connect(self.download_finished)
        self.download_thread.start()
    
    def update_progress(self, model_name, progress):
        \"\"\"Update the progress bar value\"\"\"
        if model_name == self.model_data["name"]:
            self.progress_bar.setValue(int(progress))
    
    def download_finished(self, model_name, success):
        \"\"\"Handle download completion\"\"\"
        if model_name != self.model_data["name"]:
            return
            
        self.action_button.setEnabled(True)
        
        if success:
            self.model_data["downloaded"] = True
            self.update_state()
        else:
            self.progress_bar.setVisible(False)
            QMessageBox.warning(self, "Download Failed", 
                                f"Failed to download model {model_name}. Please try again later.")
    
    def remove_model(self):
        \"\"\"Remove the downloaded model\"\"\"
        try:
            response = requests.get(f"{DEFAULT_SERVER_URL}/api/models/remove?name={self.model_data['name']}")
            response.raise_for_status()
            result = response.json()
            
            if result.get("status") == "success":
                self.model_data["downloaded"] = False
                self.update_state()
            else:
                QMessageBox.warning(self, "Remove Failed", 
                                    f"Failed to remove model: {result.get('message', 'Unknown error')}")
        except Exception as e:
            QMessageBox.warning(self, "Remove Failed", f"Failed to remove model: {str(e)}")


class KCRiffDesktop(QMainWindow):
    \"\"\"Main application window for KC-Riff Desktop\"\"\"
    
    def __init__(self):
        super().__init__()
        
        self.dark_mode = True
        self.batch_download_thread = None
        self.model_cards = {}  # Keep track of model cards by name
        
        # Set window properties
        self.setWindowTitle("KC-Riff Desktop")
        self.setMinimumSize(800, 600)
        
        # Set up UI
        self.setup_ui()
        self.apply_theme()
        
        # Load models
        self.load_models()
        
        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_models)
        self.refresh_timer.start(10000)  # Refresh every 10 seconds
    
    def setup_ui(self):
        \"\"\"Set up the main UI\"\"\"
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_layout = QHBoxLayout()
        
        logo_label = QLabel("KC-Riff")
        logo_font = QFont()
        logo_font.setPointSize(18)
        logo_font.setBold(True)
        logo_label.setFont(logo_font)
        
        theme_button = QPushButton("Toggle Theme")
        theme_button.clicked.connect(self.toggle_theme)
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh_models)
        
        header_layout.addWidget(logo_label)
        header_layout.addStretch()
        header_layout.addWidget(theme_button)
        header_layout.addWidget(refresh_button)
        main_layout.addLayout(header_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        recommended_tab = QWidget()
        all_models_tab = QWidget()
        self.tabs.addTab(recommended_tab, "Recommended")
        self.tabs.addTab(all_models_tab, "All Models")
        main_layout.addWidget(self.tabs)
        
        # Recommended tab layout
        recommended_layout = QVBoxLayout(recommended_tab)
        recommended_header = QHBoxLayout()
        recommended_label = QLabel("Recommended for KillChaos")
        rec_font = QFont()
        rec_font.setPointSize(14)
        rec_font.setBold(True)
        recommended_label.setFont(rec_font)
        
        self.download_all_button = QPushButton("Download All Recommended")
        self.download_all_button.clicked.connect(self.download_all_recommended)
        
        recommended_header.addWidget(recommended_label)
        recommended_header.addStretch()
        recommended_header.addWidget(self.download_all_button)
        recommended_layout.addLayout(recommended_header)
        
        # Scroll area for recommended models
        recommended_scroll = QScrollArea()
        recommended_scroll.setWidgetResizable(True)
        recommended_container = QWidget()
        self.recommended_grid = QGridLayout(recommended_container)
        recommended_scroll.setWidget(recommended_container)
        recommended_layout.addWidget(recommended_scroll)
        
        # All models tab layout
        all_models_layout = QVBoxLayout(all_models_tab)
        all_models_label = QLabel("All Available Models")
        all_models_label.setFont(rec_font)
        all_models_layout.addWidget(all_models_label)
        
        # Scroll area for all models
        all_models_scroll = QScrollArea()
        all_models_scroll.setWidgetResizable(True)
        all_models_container = QWidget()
        self.all_models_grid = QGridLayout(all_models_container)
        all_models_scroll.setWidget(all_models_container)
        all_models_layout.addWidget(all_models_scroll)
        
        # Batch download progress
        self.batch_progress_frame = QFrame()
        self.batch_progress_frame.setFrameShape(QFrame.StyledPanel)
        self.batch_progress_frame.setVisible(False)
        batch_progress_layout = QVBoxLayout(self.batch_progress_frame)
        
        self.batch_progress_label = QLabel("Downloading Recommended Models...")
        batch_progress_layout.addWidget(self.batch_progress_label)
        
        self.batch_progress_bar = QProgressBar()
        self.batch_progress_bar.setRange(0, 100)
        batch_progress_layout.addWidget(self.batch_progress_bar)
        
        main_layout.addWidget(self.batch_progress_frame)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def apply_theme(self):
        \"\"\"Apply the current theme to the application\"\"\"
        palette = QPalette()
        
        if self.dark_mode:
            # Dark theme
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
            # Light theme
            palette.setColor(QPalette.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(0, 100, 200))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.white)
        
        QApplication.setPalette(palette)
        
        # Update all model cards
        for card in self.model_cards.values():
            card.dark_mode = self.dark_mode
            # Re-apply styles that depend on dark mode
            if self.dark_mode:
                recommended_color = QColor(0, 180, 0)
                card.rec_label.setStyleSheet(f"color: rgb({recommended_color.red()}, {recommended_color.green()}, {recommended_color.blue()})")
            else:
                recommended_color = QColor(0, 120, 0)
                card.rec_label.setStyleSheet(f"color: rgb({recommended_color.red()}, {recommended_color.green()}, {recommended_color.blue()})")
    
    def toggle_theme(self):
        \"\"\"Switch between light and dark themes\"\"\"
        self.dark_mode = not self.dark_mode
        self.apply_theme()
    
    def load_models(self):
        \"\"\"Load models from the API\"\"\"
        try:
            response = requests.get(f"{DEFAULT_SERVER_URL}/api/models")
            response.raise_for_status()
            models = response.json()
            
            self.clear_model_grids()
            self.display_models(models, self.all_models_grid)
            
            # Display recommended models
            recommended = [m for m in models if m.get("kc_recommended", False)]
            self.display_models(recommended, self.recommended_grid, is_recommended=True)
            
            # Update status bar
            self.statusBar().showMessage(f"Loaded {len(models)} models ({len(recommended)} recommended)")
            
        except requests.exceptions.RequestException as e:
            QMessageBox.warning(self, "Connection Error", 
                               f"Could not connect to KC-Riff server: {str(e)}")
    
    def clear_model_grids(self):
        \"\"\"Clear the model grid layouts\"\"\"
        def clear_layout(layout):
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
        
        clear_layout(self.recommended_grid)
        clear_layout(self.all_models_grid)
        self.model_cards = {}
    
    def display_models(self, models, grid_layout, is_recommended=False):
        \"\"\"Display models in the specified grid layout\"\"\"
        row, col = 0, 0
        max_cols = 2
        
        for model in models:
            card = ModelCard(model, dark_mode=self.dark_mode)
            grid_layout.addWidget(card, row, col)
            self.model_cards[model["name"]] = card
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def download_all_recommended(self):
        \"\"\"Download all recommended models at once\"\"\"
        self.download_all_button.setEnabled(False)
        self.batch_progress_frame.setVisible(True)
        self.batch_progress_bar.setValue(0)
        
        self.batch_download_thread = BatchDownloadThread(download_recommended=True)
        self.batch_download_thread.progress_updated.connect(self.update_batch_progress)
        self.batch_download_thread.batch_complete.connect(self.batch_download_finished)
        self.batch_download_thread.start()
    
    def update_batch_progress(self, progress_dict):
        \"\"\"Update progress for batch download\"\"\"
        # Calculate average progress
        if not progress_dict:
            return
            
        avg_progress = sum(progress_dict.values()) / len(progress_dict)
        self.batch_progress_bar.setValue(int(avg_progress))
        
        # Also update individual model cards
        for model_name, progress in progress_dict.items():
            if model_name in self.model_cards:
                self.model_cards[model_name].update_progress(model_name, progress)
    
    def batch_download_finished(self, success, message):
        \"\"\"Handle batch download completion\"\"\"
        self.download_all_button.setEnabled(True)
        self.batch_progress_frame.setVisible(False)
        
        if success:
            self.statusBar().showMessage("All recommended models downloaded successfully")
        else:
            QMessageBox.warning(self, "Batch Download", f"Some models failed to download: {message}")
        
        # Refresh to update model states
        self.refresh_models()
    
    def refresh_models(self):
        \"\"\"Refresh model data\"\"\"
        try:
            response = requests.get(f"{DEFAULT_SERVER_URL}/api/models")
            response.raise_for_status()
            models = response.json()
            
            # Update existing cards
            for model in models:
                if model["name"] in self.model_cards:
                    self.model_cards[model["name"]].update_model_data(model)
            
        except requests.exceptions.RequestException as e:
            # Don't show error on auto-refresh
            self.statusBar().showMessage(f"Auto-refresh failed: {str(e)}")
    
    def closeEvent(self, event):
        \"\"\"Handle window close event\"\"\"
        # Stop any running threads
        if self.batch_download_thread and self.batch_download_thread.isRunning():
            self.batch_download_thread.stop()
        
        for card in self.model_cards.values():
            if card.download_thread and card.download_thread.isRunning():
                card.download_thread.stop()
        
        # Accept the close event
        event.accept()


def main():
    app = QApplication(sys.argv)
    
    # Check if server is running
    try:
        response = requests.get(f"{DEFAULT_SERVER_URL}/api/health")
        response.raise_for_status()
    except:
        QMessageBox.critical(None, "Server Not Running", 
                            "The KC-Riff server is not running. Please start it with 'go run minimal_server.go' before running this app.")
        return 1
    
    window = KCRiffDesktop()
    window.show()
    
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
""")

    # Create the run_desktop module if it doesn't exist
    run_desktop_py_path = os.path.join(pyqt_interface_dir, "run_desktop.py")
    if not os.path.exists(run_desktop_py_path):
        print("Creating run_desktop.py script...")
        
        with open(run_desktop_py_path, "w") as f:
            f.write("""#!/usr/bin/env python3
\"\"\"
Run the KC-Riff desktop application.
This script starts the PyQt-based desktop interface for KC-Riff.
\"\"\"

import os
import sys
import subprocess
import threading
import time

try:
    from PyQt5.QtWidgets import QApplication
except ImportError:
    print("PyQt5 not found. Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5"])
    from PyQt5.QtWidgets import QApplication

# Import the desktop app
from kcriff_desktop import main as desktop_main

def start_go_backend():
    \"\"\"Start the Go backend server in a separate process\"\"\"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    
    # Command to run the Go backend
    go_cmd = ["go", "run", os.path.join(repo_dir, "minimal_server.go")]
    
    # Start the process
    process = subprocess.Popen(
        go_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Monitor for startup
    def monitor_stderr():
        for line in process.stderr:
            line_str = line.decode('utf-8').strip()
            print(f"[GO SERVER] {line_str}")
            if "Starting minimal server" in line_str:
                print("KC-Riff server started successfully!")
                break
    
    # Start monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor_stderr)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # Wait for server to start
    time.sleep(1)
    
    return process

def main():
    \"\"\"Main function\"\"\"
    # Start the Go backend
    server_process = start_go_backend()
    
    try:
        # Run the desktop app
        desktop_main()
    finally:
        # Ensure server is stopped when app exits
        if server_process:
            server_process.terminate()
            server_process.wait()
            print("KC-Riff server stopped.")

if __name__ == "__main__":
    main()
""")

def start_go_backend():
    """Start the Go backend server in a separate process"""
    # Command to run the Go backend
    go_cmd = ["go", "run", "minimal_server.go"]
    
    # Start the process
    process = subprocess.Popen(
        go_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Monitor for startup
    def monitor_stderr():
        for line in process.stderr:
            line_str = line.decode('utf-8').strip()
            print(f"[GO SERVER] {line_str}")
            if "Starting minimal server" in line_str:
                print("KC-Riff minimal server started successfully!")
                break
    
    # Start monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor_stderr)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    return process

def main():
    """Main function"""
    # Start the Go backend
    print("Starting KC-Riff minimal server...")
    server_process = start_go_backend()
    
    try:
        # Use the imported desktop module
        from pyqt_interface.kcriff_desktop import main as desktop_main
        desktop_main()
    except ImportError as e:
        print(f"Error importing desktop module: {e}")
        print("Make sure PyQt5 is installed and the kcriff_desktop.py file exists in the pyqt_interface directory.")
        return 1
    finally:
        # Ensure server is stopped when app exits
        if server_process:
            server_process.terminate()
            server_process.wait()
            print("KC-Riff server stopped.")

if __name__ == "__main__":
    main()