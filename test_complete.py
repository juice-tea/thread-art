#!/usr/bin/env python3
"""
Comprehensive test of the thread art generation workflow.
"""

import os
import sys
import numpy as np

# Set Qt platform for headless testing
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

def test_workflow():
    """Test the complete thread art generation workflow."""
    print("🧵 Testing Thread Art Generation Workflow")
    print("=" * 50)
    
    # Test imports
    print("1. Testing imports...")
    try:
        from src.core.dxf_processor import DXFProcessor
        from src.core.image_processor import ImageProcessor
        from src.core.thread_art import ThreadArtGenerator
        from src.utils.csv_exporter import CSVExporter
        print("   ✓ All modules imported successfully")
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False
    
    # Test DXF processing
    print("\n2. Testing DXF processing...")
    try:
        # Test with default anchors
        anchors = DXFProcessor.create_circular_anchors(32)
        print(f"   ✓ Created {len(anchors)} default anchor points")
        
        # Test loading DXF file if it exists
        if os.path.exists('test_files/test_anchors.dxf'):
            dxf_anchors = DXFProcessor.load_anchor_points('test_files/test_anchors.dxf')
            print(f"   ✓ Loaded {len(dxf_anchors)} anchor points from DXF")
            anchors = dxf_anchors
        else:
            print("   ⚠ DXF file not found, using default anchors")
    except Exception as e:
        print(f"   ❌ DXF processing error: {e}")
        return False
    
    # Test image processing
    print("\n3. Testing image processing...")
    try:
        if os.path.exists('test_images/test_image.png'):
            processed_image = ImageProcessor.load_and_preprocess('test_images/test_image.png')
            print(f"   ✓ Processed image: {processed_image.shape}")
        else:
            # Create a simple test image
            processed_image = np.ones((400, 600), dtype=np.uint8) * 255
            # Add a simple pattern
            processed_image[150:250, 250:350] = 100
            print("   ✓ Created synthetic test image")
    except Exception as e:
        print(f"   ❌ Image processing error: {e}")
        return False
    
    # Test thread art generation
    print("\n4. Testing thread art generation...")
    try:
        generator = ThreadArtGenerator(anchors, processed_image)
        print("   ✓ ThreadArtGenerator created")
        
        # Generate with a small number of lines for testing
        path = generator.generate_path(max_lines=100, line_weight=20)
        print(f"   ✓ Generated path with {len(path)} lines")
        
        # Generate simulation
        simulation = generator.generate_simulation(path)
        print(f"   ✓ Generated simulation: {simulation.shape}")
    except Exception as e:
        print(f"   ❌ Thread art generation error: {e}")
        return False
    
    # Test CSV export
    print("\n5. Testing CSV export...")
    try:
        os.makedirs('test_output', exist_ok=True)
        
        metadata = {
            "Test Run": "Automated Test",
            "Anchor Points": len(anchors),
            "Path Length": len(path)
        }
        
        CSVExporter.export_path(
            path, anchors, 'test_output/test_path.csv', metadata
        )
        print("   ✓ Exported path to CSV")
        
        CSVExporter.export_anchor_points(anchors, 'test_output/test_anchors.csv')
        print("   ✓ Exported anchor points to CSV")
    except Exception as e:
        print(f"   ❌ CSV export error: {e}")
        return False
    
    # Test image export
    print("\n6. Testing image export...")
    try:
        ImageProcessor.save_image(simulation, 'test_output/test_simulation.png')
        print("   ✓ Exported simulation image")
    except Exception as e:
        print(f"   ❌ Image export error: {e}")
        return False
    
    print("\n🎉 All tests passed successfully!")
    print("\nGenerated files:")
    print("- test_output/test_path.csv")
    print("- test_output/test_anchors.csv") 
    print("- test_output/test_simulation.png")
    
    return True

def test_gui_components():
    """Test GUI components without actually showing the window."""
    print("\n🖥️  Testing GUI Components")
    print("=" * 30)
    
    try:
        from PySide6.QtWidgets import QApplication
        from src.gui.main_window import ThreadArtMainWindow
        
        # Create application but don't show window
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Create main window
        window = ThreadArtMainWindow()
        print("   ✓ Main window created successfully")
        
        # Test some basic functionality
        print(f"   ✓ Window title: {window.windowTitle()}")
        print(f"   ✓ Default anchors loaded: {len(window.anchor_points) if window.anchor_points else 0} points")
        
        return True
        
    except Exception as e:
        print(f"   ❌ GUI test error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Thread Art Generator - Comprehensive Testing")
    print("=" * 60)
    
    # Run workflow tests
    workflow_success = test_workflow()
    
    # Run GUI tests
    gui_success = test_gui_components()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 20)
    print(f"Workflow Test: {'✓ PASS' if workflow_success else '❌ FAIL'}")
    print(f"GUI Test: {'✓ PASS' if gui_success else '❌ FAIL'}")
    
    if workflow_success and gui_success:
        print("\n🎉 All tests passed! The Thread Art Generator is ready to use.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)