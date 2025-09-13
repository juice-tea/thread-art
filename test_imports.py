#!/usr/bin/env python3
"""
Simple test to check if PySide6 can be imported and a basic window can be created.
"""

import sys
import os

# Set Qt platform plugin
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

try:
    from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
    from PySide6.QtCore import Qt
    
    print("✓ PySide6 imports successful")
    
    app = QApplication(sys.argv)
    print("✓ QApplication created successfully")
    
    # Test basic widget creation
    widget = QWidget()
    layout = QVBoxLayout()
    label = QLabel("Test Label")
    layout.addWidget(label)
    widget.setLayout(layout)
    print("✓ Basic widget creation successful")
    
    # Test our custom modules
    from src.core.dxf_processor import DXFProcessor
    from src.core.image_processor import ImageProcessor
    from src.core.thread_art import ThreadArtGenerator
    from src.utils.csv_exporter import CSVExporter
    
    print("✓ All custom modules imported successfully")
    
    # Test anchor point creation
    anchors = DXFProcessor.create_circular_anchors(10)
    print(f"✓ Created {len(anchors)} default anchor points")
    
    print("\n🎉 All tests passed! The application should work correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)