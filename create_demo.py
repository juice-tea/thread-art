#!/usr/bin/env python3
"""
Demo of thread art generation functionality.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
from src.core.dxf_processor import DXFProcessor
from src.core.image_processor import ImageProcessor
from src.core.thread_art import ThreadArtGenerator

def create_demo():
    """Create a visual demo of the thread art generation process."""
    print("🎨 Creating Thread Art Generation Demo")
    print("=" * 40)
    
    # Load test data
    print("Loading test data...")
    anchors = DXFProcessor.create_circular_anchors(128)  # More points for better result
    if os.path.exists('test_images/test_image.png'):
        image = ImageProcessor.load_and_preprocess('test_images/test_image.png', (400, 400))
    else:
        # Create a simple test pattern
        image = np.ones((400, 400), dtype=np.uint8) * 255
        image[150:250, 150:250] = 100  # Dark square
        
    print(f"Using {len(anchors)} anchor points")
    print(f"Image size: {image.shape}")
    
    # Generate thread art
    print("Generating thread art...")
    generator = ThreadArtGenerator(anchors, image)
    path = generator.generate_path(max_lines=500, line_weight=30)
    simulation = generator.generate_simulation(path)
    
    print(f"Generated path with {len(path)} lines")
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Thread Art Generator - Demo Results', fontsize=16, fontweight='bold')
    
    # Plot 1: Anchor points
    anchor_array = np.array(anchors)
    axes[0, 0].scatter(anchor_array[:, 0], anchor_array[:, 1], s=10, c='red', alpha=0.7)
    axes[0, 0].set_title(f'Anchor Points ({len(anchors)} points)')
    axes[0, 0].set_aspect('equal')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Original image
    axes[0, 1].imshow(image, cmap='gray')
    axes[0, 1].set_title('Target Image (Processed)')
    axes[0, 1].axis('off')
    
    # Plot 3: Path visualization (first 50 lines)
    axes[1, 0].scatter(anchor_array[:, 0], anchor_array[:, 1], s=5, c='lightgray', alpha=0.5)
    for i in range(min(50, len(path) - 1)):
        p1 = anchors[path[i]]
        p2 = anchors[path[i + 1]]
        axes[1, 0].plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-', alpha=0.6, linewidth=0.5)
    axes[1, 0].set_title(f'Thread Path (first 50 of {len(path)} lines)')
    axes[1, 0].set_aspect('equal')
    
    # Plot 4: Final simulation
    axes[1, 1].imshow(simulation, cmap='gray')
    axes[1, 1].set_title('Thread Art Simulation')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    
    # Save the demo
    os.makedirs('demo_output', exist_ok=True)
    plt.savefig('demo_output/thread_art_demo.png', dpi=150, bbox_inches='tight')
    print("Demo visualization saved: demo_output/thread_art_demo.png")
    
    # Save individual images
    plt.figure(figsize=(8, 8))
    plt.imshow(simulation, cmap='gray')
    plt.title('Thread Art Simulation Result', fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.savefig('demo_output/simulation_result.png', dpi=150, bbox_inches='tight')
    print("Simulation result saved: demo_output/simulation_result.png")
    
    return True

if __name__ == "__main__":
    create_demo()
    print("\n🎉 Demo created successfully!")
    print("Check the demo_output/ directory for visualization files.")