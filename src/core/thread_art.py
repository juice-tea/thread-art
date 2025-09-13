"""
Core thread art generation logic.
"""

import numpy as np
from typing import List, Tuple, Optional
import cv2
from scipy.spatial.distance import cdist


class ThreadArtGenerator:
    """Generates thread art paths from anchor points and target image."""
    
    def __init__(self, anchor_points: List[Tuple[float, float]], image: np.ndarray):
        """
        Initialize the thread art generator.
        
        Args:
            anchor_points: List of (x, y) coordinates for anchor points
            image: Target image as numpy array (grayscale)
        """
        self.anchor_points = np.array(anchor_points)
        self.image = image
        self.path = []
        self.num_anchors = len(anchor_points)
        
    def generate_path(self, max_lines: int = 3000, line_weight: float = 25) -> List[int]:
        """
        Generate the thread path using a greedy algorithm.
        
        Args:
            max_lines: Maximum number of lines to draw
            line_weight: Weight factor for line darkness
            
        Returns:
            List of anchor point indices representing the thread path
        """
        # Create a copy of the image to work with
        current_image = self.image.copy().astype(np.float64)
        path = []
        
        # Start from the first anchor point
        current_anchor = 0
        path.append(current_anchor)
        
        for _ in range(max_lines - 1):
            best_score = -1
            best_anchor = -1
            
            # Try connecting to each other anchor point
            for next_anchor in range(self.num_anchors):
                if next_anchor == current_anchor:
                    continue
                    
                # Calculate the score for this line
                score = self._calculate_line_score(current_anchor, next_anchor, current_image)
                
                if score > best_score:
                    best_score = score
                    best_anchor = next_anchor
            
            if best_anchor == -1:
                break
                
            # Draw the line and update the working image
            self._draw_line(current_anchor, best_anchor, current_image, line_weight)
            path.append(best_anchor)
            current_anchor = best_anchor
            
        return path
    
    def _calculate_line_score(self, anchor1: int, anchor2: int, image: np.ndarray) -> float:
        """Calculate how well a line matches the target image darkness."""
        points = self._get_line_points(anchor1, anchor2)
        if len(points) == 0:
            return 0
        
        # Get pixel values along the line
        y_coords, x_coords = zip(*points)
        pixel_values = image[y_coords, x_coords]
        
        # Score is the sum of darkness (lower pixel values = higher score)
        score = np.sum(255 - pixel_values)
        return score
    
    def _draw_line(self, anchor1: int, anchor2: int, image: np.ndarray, weight: float):
        """Draw a line on the working image to simulate thread placement."""
        points = self._get_line_points(anchor1, anchor2)
        if len(points) == 0:
            return
            
        y_coords, x_coords = zip(*points)
        image[y_coords, x_coords] = np.maximum(0, image[y_coords, x_coords] - weight)
    
    def _get_line_points(self, anchor1: int, anchor2: int) -> List[Tuple[int, int]]:
        """Get pixel coordinates along a line between two anchor points."""
        p1 = self.anchor_points[anchor1]
        p2 = self.anchor_points[anchor2]
        
        # Convert to image coordinates
        h, w = self.image.shape
        x1 = int(p1[0] * w)
        y1 = int(p1[1] * h)
        x2 = int(p2[0] * w)
        y2 = int(p2[1] * h)
        
        # Bresenham's line algorithm
        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        x, y = x1, y1
        while True:
            if 0 <= x < w and 0 <= y < h:
                points.append((y, x))
                
            if x == x2 and y == y2:
                break
                
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
        
        return points
    
    def generate_simulation(self, path: List[int]) -> np.ndarray:
        """Generate a simulation image of the thread art."""
        # Start with white background
        simulation = np.ones_like(self.image) * 255
        
        # Draw each line in the path
        for i in range(len(path) - 1):
            anchor1 = path[i]
            anchor2 = path[i + 1]
            self._draw_simulation_line(anchor1, anchor2, simulation)
        
        return simulation.astype(np.uint8)
    
    def _draw_simulation_line(self, anchor1: int, anchor2: int, image: np.ndarray):
        """Draw a line on the simulation image."""
        points = self._get_line_points(anchor1, anchor2)
        if len(points) == 0:
            return
            
        y_coords, x_coords = zip(*points)
        # Make lines darker (subtract from white background)
        image[y_coords, x_coords] = np.maximum(0, image[y_coords, x_coords] - 30)