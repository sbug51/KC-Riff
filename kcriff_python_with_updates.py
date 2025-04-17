"""
KC-Riff Python Integration with Update Capability
Direct library integration for the KillChaos ecosystem
"""

import ctypes
import json
import os
import platform
import time
from ctypes import c_char_p

class KCRiffLibrary:
    """Wrapper for the KC-Riff shared library"""
    
    def __init__(self):
        # Load the shared library based on platform
        if platform.system() == "Windows":
            lib_path = os.path.join(os.path.dirname(__file__), "kcriff_updatable.dll")
            self.lib = ctypes.CDLL(lib_path)
        elif platform.system() == "Linux":
            lib_path = os.path.join(os.path.dirname(__file__), "kcriff_updatable.so")
            self.lib = ctypes.CDLL(lib_path)
        else:
            lib_path = os.path.join(os.path.dirname(__file__), "kcriff_updatable.dylib")
            self.lib = ctypes.CDLL(lib_path)
        
        # Configure function return types
        self.lib.GetModels.restype = c_char_p
        self.lib.DownloadModel.restype = c_char_p
        self.lib.GetDownloadStatus.restype = c_char_p
        self.lib.RemoveModel.restype = c_char_p
        self.lib.CheckForUpdatesC.restype = c_char_p
        self.lib.ApplyUpdate.restype = c_char_p
        self.lib.GetHealthCheck.restype = c_char_p

class KCRiff:
    """KC-Riff integration class for KillChaos with update capabilities"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KCRiff, cls).__new__(cls)
            cls._instance.lib = KCRiffLibrary()
        return cls._instance
    
    def get_models(self):
        """Get available models"""
        result = self.lib.lib.GetModels()
        return json.loads(result.decode('utf-8'))
    
    def download_model(self, model_name):
        """Start downloading a model"""
        result = self.lib.lib.DownloadModel(model_name.encode('utf-8'))
        return json.loads(result.decode('utf-8'))
    
    def get_download_status(self, model_name):
        """Get download status for a model"""
        result = self.lib.lib.GetDownloadStatus(model_name.encode('utf-8'))
        return json.loads(result.decode('utf-8'))
    
    def remove_model(self, model_name):
        """Remove a downloaded model"""
        result = self.lib.lib.RemoveModel(model_name.encode('utf-8'))
        return json.loads(result.decode('utf-8'))
    
    def check_for_updates(self):
        """Check if updates are available"""
        result = self.lib.lib.CheckForUpdatesC()
        return json.loads(result.decode('utf-8'))
    
    def apply_update(self):
        """Apply available updates"""
        result = self.lib.lib.ApplyUpdate()
        return json.loads(result.decode('utf-8'))
    
    def health_check(self):
        """Check if KC-Riff is functional"""
        result = self.lib.lib.GetHealthCheck()
        return json.loads(result.decode('utf-8'))
    
    def wait_for_download_completion(self, model_name, progress_callback=None, timeout=300):
        """Wait for a model download to complete, with optional progress callback"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.get_download_status(model_name)
            if "error" in status:
                return False, status["error"]
            
            if progress_callback:
                progress_callback(status["progress"])
            
            if status.get("completed", False):
                return True, "Download complete"
            
            time.sleep(1)
        
        return False, "Download timed out"

# Example of how you might integrate this with KillChaos
class KillChaosModelManager:
    """Example integration class for KillChaos"""
    
    def __init__(self):
        self.kcriff = KCRiff()
    
    def initialize(self):
        """Initialize the model manager"""
        health = self.kcriff.health_check()
        if health["status"] != "ok":
            raise Exception(f"KC-Riff health check failed: {health}")
        
        # Check for updates on initialization
        update_info = self.kcriff.check_for_updates()
        if update_info.get("available", False):
            print(f"KC-Riff update available: {update_info['new_version']}")
            # You can decide to prompt the user or apply automatically
    
    def get_available_models(self):
        """Get all available models"""
        return self.kcriff.get_models()
    
    def get_recommended_models(self):
        """Get recommended models only"""
        all_models = self.kcriff.get_models()
        return [m for m in all_models if m.get("recommended", False)]
    
    def get_downloaded_models(self):
        """Get models that have been downloaded"""
        all_models = self.kcriff.get_models()
        return [m for m in all_models if m.get("downloaded", False)]
    
    def download_model(self, model_name, show_progress=True):
        """Download a model with optional progress display"""
        self.kcriff.download_model(model_name)
        
        if show_progress:
            def update_progress(progress):
                print(f"\rDownloading {model_name}: {progress:.1f}%", end="")
            
            success, message = self.kcriff.wait_for_download_completion(
                model_name, 
                progress_callback=update_progress
            )
            
            print()  # New line after progress display
            if success:
                print(f"Model {model_name} downloaded successfully")
            else:
                print(f"Error downloading {model_name}: {message}")
            
            return success
        
        return True  # Just started the download

# Example usage
if __name__ == "__main__":
    model_manager = KillChaosModelManager()
    model_manager.initialize()
    
    print("Available models:")
    for model in model_manager.get_available_models():
        print(f"- {model['name']}: {model['description']}")
    
    print("\nRecommended models:")
    for model in model_manager.get_recommended_models():
        print(f"- {model['name']}")
    
    # Download a model with progress display
    model_manager.download_model("llama2")
