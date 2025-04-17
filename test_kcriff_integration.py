"""
Test script for KC-Riff integration with KillChaos
"""

from kcriff_python_with_updates import KCRiff, KillChaosModelManager

def test_direct_library_usage():
    """Test direct usage of the KC-Riff library"""
    print("=== Testing Direct KC-Riff Library Usage ===")
    
    kcriff = KCRiff()
    health = kcriff.health_check()
    print(f"Health status: {health['status']}, Version: {health['version']}")
    
    models = kcriff.get_models()
    print(f"Found {len(models)} models")
    for model in models[:2]:  # Show first two
        print(f"- {model['name']}: {model['description']}")
    
    print("Testing update check...")
    update_info = kcriff.check_for_updates()
    if update_info.get("available", False):
        print(f"Update available: {update_info['new_version']}")
        print(f"Release notes: {update_info['release_notes']}")
    else:
        print("No updates available")

def test_killchaos_integration():
    """Test integration with KillChaos model manager"""
    print("\n=== Testing KillChaos Integration ===")
    
    model_manager = KillChaosModelManager()
    model_manager.initialize()
    
    print("Recommended models:")
    for model in model_manager.get_recommended_models():
        print(f"- {model['name']}")
    
    print("\nDownloading a test model...")
    model_manager.download_model("orca-mini")

if __name__ == "__main__":
    # Test direct library usage
    test_direct_library_usage()
    
    # Test KillChaos integration
    test_killchaos_integration()
