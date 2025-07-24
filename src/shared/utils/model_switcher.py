"""
Model switcher utility for easy local testing
"""
import os

# Available models
MODELS = {
    "sonnet_35": "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "sonnet_40": "anthropic.claude-sonnet-4-20250514-v1:0", 
    "haiku_35": "anthropic.claude-3-5-haiku-20241022-v1:0",
    "haiku_30": "anthropic.claude-3-haiku-20240307-v1:0"
}

def get_model_id(model_name):
    """Get the full model ID for a given model name"""
    return MODELS.get(model_name, MODELS["haiku_35"])

def list_available_models():
    """List all available models"""
    print("Available models:")
    for name, model_id in MODELS.items():
        print(f"  {name}: {model_id}")

def set_test_model(model_name):
    """Set environment variable for testing"""
    if model_name in MODELS:
        os.environ["TEST_MODEL"] = model_name
        print(f"✅ Test model set to: {model_name}")
        return True
    else:
        print(f"❌ Unknown model: {model_name}")
        list_available_models()
        return False