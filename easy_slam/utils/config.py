"""
YAML configuration utilities.
"""

import os
import yaml
from typing import Dict, Any

def load_config(path: str) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        path: Path to YAML configuration file
        
    Returns:
        Configuration dictionary
    """
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found: {path}")
        
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"[Config] Loaded configuration from {path}")
        return config
        
    except Exception as e:
        print(f"[Config] Error loading config: {e}")
        return {}

def save_config(config: Dict[str, Any], path: str):
    """
    Save configuration to YAML file.
    
    Args:
        config: Configuration dictionary
        path: Path to save YAML file
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        print(f"[Config] Saved configuration to {path}")
        
    except Exception as e:
        print(f"[Config] Error saving config: {e}")

def merge_configs(base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two configuration dictionaries.
    
    Args:
        base_config: Base configuration
        override_config: Configuration to override with
        
    Returns:
        Merged configuration
    """
    merged = base_config.copy()
    
    for key, value in override_config.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_configs(merged[key], value)
        else:
            merged[key] = value
    
    return merged 