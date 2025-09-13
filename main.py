#!/usr/bin/env python3
"""
Thread Art Generator - Main Application Entry Point

This application generates thread art paths from anchor points (DXF) and a target image,
outputting CSV path data and a simulation of the final thread art.
"""

import sys
from PySide6.QtWidgets import QApplication
from src.gui.main_window import ThreadArtMainWindow


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("Thread Art Generator")
    app.setApplicationVersion("1.0.0")
    
    window = ThreadArtMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()