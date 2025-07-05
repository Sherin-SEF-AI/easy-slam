#!/usr/bin/env python3
"""
Test script to identify GUI errors
"""

import sys
import traceback
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

def test_gui():
    try:
        app = QApplication(sys.argv)
        
        # Import and test GUI components
        print("[TEST] Testing GUI imports...")
        
        try:
            from easy_slam.gui.main_window import EasySLAMMainWindow
            print("[TEST] ✓ EasySLAMMainWindow imported successfully")
        except Exception as e:
            print(f"[TEST] ✗ Failed to import EasySLAMMainWindow: {e}")
            traceback.print_exc()
            return
        
        try:
            print("[TEST] Creating GUI window...")
            window = EasySLAMMainWindow()
            print("[TEST] ✓ GUI window created successfully")
        except Exception as e:
            print(f"[TEST] ✗ Failed to create GUI window: {e}")
            traceback.print_exc()
            return
        
        try:
            print("[TEST] Showing GUI window...")
            window.show()
            print("[TEST] ✓ GUI window shown successfully")
        except Exception as e:
            print(f"[TEST] ✗ Failed to show GUI window: {e}")
            traceback.print_exc()
            return
        
        # Set up a timer to close after 5 seconds for testing
        def close_test():
            print("[TEST] Closing test GUI...")
            app.quit()
        
        timer = QTimer()
        timer.timeout.connect(close_test)
        timer.start(5000)  # 5 seconds
        
        print("[TEST] Starting GUI event loop...")
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"[TEST] ✗ Critical error in test: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_gui() 