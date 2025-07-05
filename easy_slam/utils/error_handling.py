"""
Error handling utilities.
"""

import traceback
import sys
from typing import Optional, Dict, Any

# Error solutions database
ERROR_SOLUTIONS = {
    "camera_not_found": {
        "message": "Camera device not found or not accessible",
        "solutions": [
            "Check if camera is connected and not in use by another application",
            "Try different camera index (0, 1, 2, etc.)",
            "Install camera drivers if needed",
            "On Linux, check permissions: sudo usermod -a -G video $USER"
        ]
    },
    "insufficient_features": {
        "message": "Not enough features detected for SLAM",
        "solutions": [
            "Ensure good lighting conditions",
            "Move camera slowly to capture more features",
            "Check if scene has enough texture and structure",
            "Try adjusting camera parameters"
        ]
    },
    "tracking_lost": {
        "message": "SLAM tracking lost",
        "solutions": [
            "Move camera back to previously seen area",
            "Ensure sufficient lighting",
            "Reduce camera movement speed",
            "Check for motion blur"
        ]
    },
    "memory_error": {
        "message": "Insufficient memory for SLAM processing",
        "solutions": [
            "Reduce image resolution",
            "Close other applications",
            "Increase system memory",
            "Use offline processing mode"
        ]
    },
    "config_error": {
        "message": "Configuration file error",
        "solutions": [
            "Check YAML syntax in config file",
            "Verify all required parameters are present",
            "Use default configuration as template",
            "Check file permissions"
        ]
    }
}

def handle_error(error: Exception, context: str = "", show_traceback: bool = False) -> None:
    """
    Handle and display error with helpful solutions.
    
    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
        show_traceback: Whether to show full traceback
    """
    error_type = type(error).__name__
    error_msg = str(error)
    
    print(f"\n[ERROR] {error_type}: {error_msg}")
    if context:
        print(f"[CONTEXT] {context}")
    
    # Try to match error with known solutions
    solution_found = False
    for error_key, solution_info in ERROR_SOLUTIONS.items():
        if error_key.lower() in error_msg.lower() or error_key.lower() in error_type.lower():
            print(f"\n[SOLUTION] {solution_info['message']}")
            print("Possible solutions:")
            for i, solution in enumerate(solution_info['solutions'], 1):
                print(f"  {i}. {solution}")
            solution_found = True
            break
    
    if not solution_found:
        print("\n[GENERAL SOLUTIONS]")
        print("1. Check if all dependencies are installed")
        print("2. Verify input data format and quality")
        print("3. Try with different parameters")
        print("4. Check system resources (CPU, memory)")
    
    if show_traceback:
        print(f"\n[TRACEBACK]")
        traceback.print_exc()
    
    print()  # Empty line for readability

def check_system_requirements() -> Dict[str, bool]:
    """
    Check if system meets requirements for easy-slam.
    
    Returns:
        Dictionary with requirement check results
    """
    requirements = {
        "opencv": False,
        "numpy": False,
        "camera_access": False,
        "memory": False
    }
    
    try:
        import cv2
        requirements["opencv"] = True
    except ImportError:
        pass
    
    try:
        import numpy
        requirements["numpy"] = True
    except ImportError:
        pass
    
    # Check camera access
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            requirements["camera_access"] = True
            cap.release()
    except:
        pass
    
    # Check memory (simplified)
    try:
        import psutil
        memory_gb = psutil.virtual_memory().total / (1024**3)
        requirements["memory"] = memory_gb >= 2.0  # At least 2GB
    except:
        requirements["memory"] = True  # Assume OK if can't check
    
    return requirements

def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration dictionary.
    
    Args:
        config: Configuration to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_keys = ['slam', 'sensor']
    
    for key in required_keys:
        if key not in config:
            print(f"[CONFIG ERROR] Missing required key: {key}")
            return False
    
    # Validate sensor configuration
    if 'sensor' in config:
        sensor_config = config['sensor']
        if 'type' not in sensor_config:
            print("[CONFIG ERROR] Sensor type not specified")
            return False
    
    # Validate SLAM configuration
    if 'slam' in config:
        slam_config = config['slam']
        if 'algorithm' not in slam_config:
            print("[CONFIG ERROR] SLAM algorithm not specified")
            return False
    
    return True

def log_error(error: Exception, log_file: str = "easy_slam_errors.log") -> None:
    """
    Log error to file for debugging.
    
    Args:
        error: The exception to log
        log_file: Path to log file
    """
    try:
        import datetime
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_info = f"[{timestamp}] {type(error).__name__}: {str(error)}\n"
        
        with open(log_file, 'a') as f:
            f.write(error_info)
            f.write(traceback.format_exc())
            f.write("\n" + "="*50 + "\n")
            
    except Exception as e:
        print(f"[ERROR] Failed to log error: {e}")

def create_error_report(error: Exception, context: str = "") -> str:
    """
    Create a detailed error report for debugging.
    
    Args:
        error: The exception that occurred
        context: Additional context
        
    Returns:
        Formatted error report string
    """
    import platform
    import sys
    
    report = []
    report.append("=" * 60)
    report.append("EASY-SLAM ERROR REPORT")
    report.append("=" * 60)
    report.append(f"Error Type: {type(error).__name__}")
    report.append(f"Error Message: {str(error)}")
    report.append(f"Context: {context}")
    report.append(f"Platform: {platform.platform()}")
    report.append(f"Python Version: {sys.version}")
    report.append(f"Python Path: {sys.executable}")
    
    # System requirements
    requirements = check_system_requirements()
    report.append("\nSystem Requirements:")
    for req, status in requirements.items():
        report.append(f"  {req}: {'✓' if status else '✗'}")
    
    # Traceback
    report.append("\nTraceback:")
    report.append(traceback.format_exc())
    report.append("=" * 60)
    
    return "\n".join(report) 