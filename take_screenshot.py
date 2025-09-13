#!/usr/bin/env python3
"""
Screenshot demo of the Thread Art Generator application.
"""

import sys
import os
import time

# Set up display environment
os.environ['QT_QPA_PLATFORM'] = 'xcb'
os.environ['DISPLAY'] = ':1'

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from src.gui.main_window import ThreadArtMainWindow

def take_screenshot():
    """Take a screenshot of the application."""
    app = QApplication(sys.argv)
    
    # Create and show the main window
    window = ThreadArtMainWindow()
    window.show()
    
    # Load test files to show functionality
    if os.path.exists('test_images/test_image.png'):
        # Simulate loading an image
        from src.core.image_processor import ImageProcessor
        processed_image = ImageProcessor.load_and_preprocess('test_images/test_image.png')
        window.processed_image = processed_image
        window.input_image = 'test_images/test_image.png'
        window.image_label.setText("test_image.png")
        window.original_display.set_image(processed_image)
        window._check_ready_to_generate()
    
    # Take screenshot after a brief delay
    def screenshot_timer():
        pixmap = window.grab()
        pixmap.save('screenshots/main_window.png')
        print("Screenshot saved: screenshots/main_window.png")
        app.quit()
    
    # Create output directory
    os.makedirs('screenshots', exist_ok=True)
    
    # Schedule screenshot
    QTimer.singleShot(1000, screenshot_timer)
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    take_screenshot()