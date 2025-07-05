from .main_window import EasySLAMMainWindow
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    window = EasySLAMMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 