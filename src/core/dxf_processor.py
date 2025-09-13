"""
DXF file processing for anchor points.
"""

import ezdxf
from typing import List, Tuple, Optional
import numpy as np


class DXFProcessor:
    """Processes DXF files to extract anchor points."""
    
    @staticmethod
    def load_anchor_points(file_path: str) -> List[Tuple[float, float]]:
        """
        Load anchor points from a DXF file.
        
        Args:
            file_path: Path to the DXF file
            
        Returns:
            List of (x, y) coordinates normalized to [0, 1] range
        """
        try:
            doc = ezdxf.readfile(file_path)
            modelspace = doc.modelspace()
            
            points = []
            
            # Extract points from various DXF entities
            for entity in modelspace:
                if entity.dxftype() == 'POINT':
                    point = entity.dxf.location
                    points.append((point.x, point.y))
                elif entity.dxftype() == 'CIRCLE':
                    center = entity.dxf.center
                    points.append((center.x, center.y))
                elif entity.dxftype() == 'LINE':
                    # Add both endpoints of lines as potential anchor points
                    start = entity.dxf.start
                    end = entity.dxf.end
                    points.append((start.x, start.y))
                    points.append((end.x, end.y))
                elif entity.dxftype() == 'LWPOLYLINE' or entity.dxftype() == 'POLYLINE':
                    # Add vertices of polylines
                    for point in entity.get_points():
                        points.append((point[0], point[1]))
            
            if not points:
                raise ValueError("No anchor points found in DXF file")
            
            # Normalize points to [0, 1] range
            points_array = np.array(points)
            min_vals = points_array.min(axis=0)
            max_vals = points_array.max(axis=0)
            
            # Handle case where all points are the same
            ranges = max_vals - min_vals
            ranges[ranges == 0] = 1
            
            normalized_points = (points_array - min_vals) / ranges
            
            return normalized_points.tolist()
            
        except Exception as e:
            raise RuntimeError(f"Error processing DXF file: {str(e)}")
    
    @staticmethod
    def create_circular_anchors(num_points: int = 256) -> List[Tuple[float, float]]:
        """
        Create anchor points arranged in a circle (default/fallback option).
        
        Args:
            num_points: Number of anchor points to create
            
        Returns:
            List of (x, y) coordinates normalized to [0, 1] range
        """
        angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
        
        # Create points on a circle centered at (0.5, 0.5) with radius 0.4
        x_coords = 0.5 + 0.4 * np.cos(angles)
        y_coords = 0.5 + 0.4 * np.sin(angles)
        
        return list(zip(x_coords, y_coords))