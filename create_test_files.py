#!/usr/bin/env python3
"""
Create test files for the thread art application.
"""

import numpy as np
import cv2
import ezdxf
from PIL import Image, ImageDraw
import os

def create_test_image():
    """Create a test image for thread art generation."""
    # Create a simple test image with geometric patterns
    width, height = 800, 600
    
    # Create image using PIL
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw a circle
    center_x, center_y = width // 2, height // 2
    radius = min(width, height) // 4
    draw.ellipse([center_x - radius, center_y - radius, 
                  center_x + radius, center_y + radius], 
                 outline='black', width=3)
    
    # Draw some lines to create interesting patterns
    for i in range(8):
        angle = i * np.pi / 4
        x1 = center_x + int(radius * 0.7 * np.cos(angle))
        y1 = center_y + int(radius * 0.7 * np.sin(angle))
        x2 = center_x + int(radius * 1.3 * np.cos(angle))
        y2 = center_y + int(radius * 1.3 * np.sin(angle))
        draw.line([x1, y1, x2, y2], fill='black', width=2)
    
    # Add some text
    try:
        # Try to draw some text
        draw.text((center_x - 50, center_y + radius + 20), 
                 "Thread Art", fill='black')
    except:
        # If font is not available, skip text
        pass
    
    # Save the image
    img.save('test_images/test_image.png')
    print("✓ Created test image: test_images/test_image.png")

def create_test_dxf():
    """Create a test DXF file with anchor points."""
    # Create new DXF document
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Create anchor points in a circle
    num_points = 64
    radius = 50
    center_x, center_y = 0, 0
    
    for i in range(num_points):
        angle = 2 * np.pi * i / num_points
        x = center_x + radius * np.cos(angle)
        y = center_y + radius * np.sin(angle)
        
        # Add a point
        msp.add_point((x, y))
    
    # Add some additional points for variety
    # Inner circle
    inner_radius = 25
    for i in range(0, num_points, 4):  # Every 4th point
        angle = 2 * np.pi * i / num_points
        x = center_x + inner_radius * np.cos(angle)
        y = center_y + inner_radius * np.sin(angle)
        msp.add_circle((x, y), 0.5)  # Small circles as anchor points
    
    # Save the DXF file
    doc.saveas('test_files/test_anchors.dxf')
    print("✓ Created test DXF: test_files/test_anchors.dxf")

def create_complex_test_image():
    """Create a more complex test image."""
    width, height = 800, 600
    
    # Create image with OpenCV for more complex patterns
    img = np.ones((height, width), dtype=np.uint8) * 255
    
    # Draw a portrait-like pattern
    center_x, center_y = width // 2, height // 2
    
    # Face outline
    cv2.ellipse(img, (center_x, center_y), (120, 160), 0, 0, 360, 100, -1)
    cv2.ellipse(img, (center_x, center_y), (110, 150), 0, 0, 360, 255, -1)
    
    # Eyes
    cv2.circle(img, (center_x - 40, center_y - 30), 15, 50, -1)
    cv2.circle(img, (center_x + 40, center_y - 30), 15, 50, -1)
    
    # Nose
    cv2.line(img, (center_x, center_y - 10), (center_x - 5, center_y + 20), 100, 2)
    
    # Mouth
    cv2.ellipse(img, (center_x, center_y + 40), (30, 15), 0, 0, 180, 80, 2)
    
    # Save the image
    cv2.imwrite('test_images/portrait_test.png', img)
    print("✓ Created complex test image: test_images/portrait_test.png")

if __name__ == "__main__":
    # Create directories
    os.makedirs('test_images', exist_ok=True)
    os.makedirs('test_files', exist_ok=True)
    
    # Create test files
    create_test_image()
    create_test_dxf()
    create_complex_test_image()
    
    print("\n🎉 All test files created successfully!")
    print("You can now use these files to test the Thread Art Generator:")
    print("- DXF file: test_files/test_anchors.dxf")
    print("- Test images: test_images/test_image.png, test_images/portrait_test.png")