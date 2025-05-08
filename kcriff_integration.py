#!/usr/bin/env python3
"""
KC-Riff Python Integration with Update Capability
Direct library integration for the KillChaos ecosystem
"""

import os
import sys
import json
import time
import ctypes
import platform
import requests
from ctypes import c_char_p, c_int, c_float, c_bool, Structure, POINTER, byref
from typing import List, Dict, Optional, Callable, Any

# Determine the correct library extension based on the platform
if platform.system() == "Windows":
    LIB_EXTENSION = ".dll"
elif platform.system() == "Darwin":
    LIB_EXTENSION = ".dylib"
else:
    LIB_EXTENSION = ".so"

LIB_PREFIX = "libkcriff" if platform.system() != "Windows" else "kcriff"

class KCRiffLibrary:
    """Wrapper for the KC-Riff shared library"""
    
    def __init__(self):
        # Try to load the library from several possible locations
        lib_paths = [
            # Current directory
            os.path.join(os.getcwd(), f"{LIB_PREFIX}{LIB_EXTENSION}"),
            # Build directory
            os.path.join(os.getcwd(), "build", f"{LIB_PREFIX}{LIB_EXTENSION}"),
            # System library paths (Linux/macOS)
            f"/usr/lib/{LIB_PREFIX}{LIB_EXTENSION}",
            f"/usr/local/lib/{LIB_PREFIX}{LIB_EXTENSION}",
            # Lib directory relative to script
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib", f"{LIB_PREFIX}{LIB_EXTENSION}"),
            # Windows system directory
            os.path.join(os.environ.get("SYSTEMROOT", "C:\\Windows"), "System32", f"{LIB_PREFIX}{LIB_EXTENSION}"),
        ]
        
        self.lib = None
        self.error_message = ""
        
        for path in lib_paths:
            try:
                self.lib = ctypes.CDLL(path)
                break
            except (OSError, FileNotFoundError):
                continue
        
        if self.lib is None:
            self.error_message = "Failed to load KC-Riff library. Falling back to HTTP API."
            # Will fall back to HTTP API mode
            return
        
        # Define function signatures
        try:
            # GetModels returns a JSON string of available models
            self.lib.GetModels.restype = c_char_p
            self.lib.GetModels.argtypes = []
            
            # StartModelDownload initiates a model download
            self.lib.StartModelDownload.restype = c_char_p
            self.lib.StartModelDownload.argtypes = [c_char_p]
            
            # GetDownloadStatus returns the status of a model download
            self.lib.GetDownloadStatus.restype = c_char_p
            self.lib.GetDownloadStatus.argtypes = [c_char_p]
            
            # RemoveModel deletes a downloaded model
            self.lib.RemoveModel.restype = c_char_p
            self.lib.RemoveModel.argtypes = [c_char_p]
            
            # CheckForUpdates checks if updates are available
            self.lib.CheckForUpdates.restype = c_char_p
            self.lib.CheckForUpdates.argtypes = []
            
            # ApplyUpdate applies available updates
            self.lib.ApplyUpdate.restype = c_char_p
            self.lib.ApplyUpdate.argtypes = []
            
            # HealthCheck checks if the library is functional
            self.lib.HealthCheck.restype = c_char_p
            self.lib.HealthCheck.argtypes = []
        except AttributeError as e:
            self.error_message = f"Failed to setup KC-Riff library functions: {str(e)}"
            self.lib = None


class KCRiff:
    """KC-Riff integration class for KillChaos with update capabilities"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KCRiff, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the KC-Riff integration"""
        self.lib_wrapper = KCRiffLibrary()
        
        # Check if we're using the library or HTTP API
        self.using_library = self.lib_wrapper.lib is not None
        
        if not self.using_library:
            print(f"Warning: {self.lib_wrapper.error_message}")
            # Default API endpoint
            self.api_url = "http://localhost:5000"
    
    def get_models(self) -> List[Dict[str, Any]]:
        """Get available models"""
        if self.using_library:
            try:
                result = self.lib_wrapper.lib.GetModels()
                if result:
                    return json.loads(result.decode('utf-8'))
                return []
            except Exception as e:
                print(f"Error calling GetModels: {str(e)}")
                return []
        else:
            # Fallback to HTTP API
            try:
                response = requests.get(f"{self.api_url}/api/models")
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"Error fetching models from API: {str(e)}")
                return []
    
    def download_model(self, model_name: str) -> Dict[str, Any]:
        """Start downloading a model"""
        if self.using_library:
            try:
                encoded_name = model_name.encode('utf-8')
                result = self.lib_wrapper.lib.StartModelDownload(encoded_name)
                if result:
                    return json.loads(result.decode('utf-8'))
                return {"error": "Failed to start download"}
            except Exception as e:
                print(f"Error calling StartModelDownload: {str(e)}")
                return {"error": str(e)}
        else:
            # Fallback to HTTP API
            try:
                response = requests.get(f"{self.api_url}/api/models/download?name={model_name}")
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"Error starting download from API: {str(e)}")
                return {"error": str(e)}
    
    def get_download_status(self, model_name: str) -> Dict[str, Any]:
        """Get download status for a model"""
        if self.using_library:
            try:
                encoded_name = model_name.encode('utf-8')
                result = self.lib_wrapper.lib.GetDownloadStatus(encoded_name)
                if result:
                    return json.loads(result.decode('utf-8'))
                return {"error": "Failed to get download status"}
            except Exception as e:
                print(f"Error calling GetDownloadStatus: {str(e)}")
                return {"error": str(e)}
        else:
            # Fallback to HTTP API
            try:
                response = requests.get(f"{self.api_url}/api/models/status?name={model_name}")
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"Error getting download status from API: {str(e)}")
                return {"error": str(e)}
    
    def remove_model(self, model_name: str) -> Dict[str, Any]:
        """Remove a downloaded model"""
        if self.using_library:
            try:
                encoded_name = model_name.encode('utf-8')
                result = self.lib_wrapper.lib.RemoveModel(encoded_name)
                if result:
                    return json.loads(result.decode('utf-8'))
                return {"error": "Failed to remove model"}
            except Exception as e:
                print(f"Error calling RemoveModel: {str(e)}")
                return {"error": str(e)}
        else:
            # Fallback to HTTP API
            try:
                response = requests.get(f"{self.api_url}/api/models/remove?name={model_name}")
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"Error removing model from API: {str(e)}")
                return {"error": str(e)}
    
    def check_for_updates(self) -> Dict[str, Any]:
        """Check if updates are available"""
        if self.using_library:
            try:
                result = self.lib_wrapper.lib.CheckForUpdates()
                if result:
                    return json.loads(result.decode('utf-8'))
                return {"available": False, "error": "Failed to check for updates"}
            except Exception as e:
                print(f"Error calling CheckForUpdates: {str(e)}")
                return {"available": False, "error": str(e)}
        else:
            # Fallback to HTTP API
            try:
                response = requests.get(f"{self.api_url}/api/updates")
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"Error checking for updates from API: {str(e)}")
                return {"available": False, "error": str(e)}
    
    def apply_update(self) -> Dict[str, Any]:
        """Apply available updates"""
        if self.using_library:
            try:
                result = self.lib_wrapper.lib.ApplyUpdate()
                if result:
                    return json.loads(result.decode('utf-8'))
                return {"status": "failed", "error": "Failed to apply update"}
            except Exception as e:
                print(f"Error calling ApplyUpdate: {str(e)}")
                return {"status": "failed", "error": str(e)}
        else:
            # Fallback to HTTP API
            try:
                response = requests.get(f"{self.api_url}/api/updates/apply")
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"Error applying update from API: {str(e)}")
                return {"status": "failed", "error": str(e)}
    
    def health_check(self) -> Dict[str, Any]:
        """Check if KC-Riff is functional"""
        if self.using_library:
            try:
                result = self.lib_wrapper.lib.HealthCheck()
                if result:
                    return json.loads(result.decode('utf-8'))
                return {"status": "unhealthy", "error": "Failed to perform health check"}
            except Exception as e:
                print(f"Error calling HealthCheck: {str(e)}")
                return {"status": "unhealthy", "error": str(e)}
        else:
            # Fallback to HTTP API
            try:
                response = requests.get(f"{self.api_url}/api/health")
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"Error performing health check from API: {str(e)}")
                return {"status": "unhealthy", "error": str(e)}
    
    def wait_for_download_completion(self, model_name: str, progress_callback: Optional[Callable[[float], None]] = None, timeout: int = 300) -> Dict[str, Any]:
        """Wait for a model download to complete, with optional progress callback"""
        start_time = time.time()
        last_progress = -1
        
        while time.time() - start_time < timeout:
            status = self.get_download_status(model_name)
            
            if "error" in status:
                return status
            
            progress = status.get("progress", 0)
            if progress != last_progress and progress_callback:
                progress_callback(progress)
                last_progress = progress
            
            if status.get("completed", False):
                return status
            
            time.sleep(0.5)
        
        return {"error": "Download timed out", "completed": False, "status": "timeout"}


class KillChaosModelManager:
    """Integration class for KillChaos"""
    
    def __init__(self):
        """Initialize with KC-Riff integration"""
        self.kcriff = None
    
    def initialize(self):
        """Initialize the model manager"""
        self.kcriff = KCRiff()
        return self.health_check()
    
    def health_check(self):
        """Check if the model manager is functional"""
        if not self.kcriff:
            return False
        
        health = self.kcriff.health_check()
        return health.get("status") == "healthy"
    
    def get_available_models(self):
        """Get all available models"""
        if not self.kcriff:
            return []
        
        return self.kcriff.get_models()
    
    def get_recommended_models(self):
        """Get recommended models only"""
        models = self.get_available_models()
        return [m for m in models if m.get("kc_recommended", False)]
    
    def get_downloaded_models(self):
        """Get models that have been downloaded"""
        models = self.get_available_models()
        return [m for m in models if m.get("downloaded", False)]
    
    def download_model(self, model_name: str, show_progress: bool = True):
        """Download a model with optional progress display"""
        if not self.kcriff:
            return {"error": "Model manager not initialized"}
        
        # Start the download
        result = self.kcriff.download_model(model_name)
        
        if "error" in result:
            return result
        
        if not show_progress:
            return result
        
        # Define progress callback
        def update_progress(progress):
            # Print progress bar
            bar_length = 40
            filled_length = int(bar_length * progress / 100)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            print(f"\rDownloading {model_name}: [{bar}] {progress:.1f}%", end='', flush=True)
        
        # Wait for completion with progress updates
        result = self.kcriff.wait_for_download_completion(model_name, update_progress)
        print()  # New line after progress bar
        
        if result.get("status") == "completed":
            print(f"Download of {model_name} completed successfully.")
        else:
            print(f"Download failed or timed out: {result.get('error', 'Unknown error')}")
        
        return result
    
    def remove_model(self, model_name: str):
        """Remove a downloaded model"""
        if not self.kcriff:
            return {"error": "Model manager not initialized"}
        
        return self.kcriff.remove_model(model_name)
    
    def check_for_updates(self):
        """Check for KC-Riff updates"""
        if not self.kcriff:
            return {"available": False, "error": "Model manager not initialized"}
        
        return self.kcriff.check_for_updates()
    
    def apply_update(self):
        """Apply available updates"""
        if not self.kcriff:
            return {"status": "failed", "error": "Model manager not initialized"}
        
        return self.kcriff.apply_update()


# Simple test if run directly
if __name__ == "__main__":
    print("KC-Riff Python Integration")
    manager = KillChaosModelManager()
    if manager.initialize():
        print("Model manager initialized successfully.")
        print("\nAvailable models:")
        models = manager.get_available_models()
        for model in models:
            print(f"- {model['name']}: {model['description']} {'[Downloaded]' if model.get('downloaded', False) else ''}")
        
        # Check for updates
        updates = manager.check_for_updates()
        if updates.get("available", False):
            print(f"\nUpdate available: version {updates.get('new_version')}")
            print(f"Release notes: {updates.get('release_notes')}")
    else:
        print("Failed to initialize model manager.")