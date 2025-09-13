"""
CSV export utilities for thread art paths.
"""

import csv
from typing import List, Tuple
from datetime import datetime


class CSVExporter:
    """Exports thread art paths to CSV format."""
    
    @staticmethod
    def export_path(path: List[int], anchor_points: List[Tuple[float, float]], 
                   file_path: str, metadata: dict = None):
        """
        Export thread path to CSV file.
        
        Args:
            path: List of anchor point indices
            anchor_points: List of (x, y) coordinates for anchor points
            file_path: Output CSV file path
            metadata: Optional metadata to include in header
        """
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header with metadata
                writer.writerow(['# Thread Art Path Export'])
                writer.writerow([f'# Generated: {datetime.now().isoformat()}'])
                
                if metadata:
                    for key, value in metadata.items():
                        writer.writerow([f'# {key}: {value}'])
                
                writer.writerow(['#'])
                writer.writerow(['# Path Data: Step, Anchor_Index, X_Coordinate, Y_Coordinate'])
                
                # Column headers
                writer.writerow(['Step', 'Anchor_Index', 'X_Coordinate', 'Y_Coordinate'])
                
                # Write path data
                for step, anchor_idx in enumerate(path):
                    if anchor_idx < len(anchor_points):
                        x, y = anchor_points[anchor_idx]
                        writer.writerow([step, anchor_idx, f'{x:.6f}', f'{y:.6f}'])
                
        except Exception as e:
            raise RuntimeError(f"Error exporting CSV: {str(e)}")
    
    @staticmethod
    def export_anchor_points(anchor_points: List[Tuple[float, float]], file_path: str):
        """
        Export anchor points to CSV file.
        
        Args:
            anchor_points: List of (x, y) coordinates
            file_path: Output CSV file path
        """
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['# Anchor Points Export'])
                writer.writerow([f'# Generated: {datetime.now().isoformat()}'])
                writer.writerow(['#'])
                writer.writerow(['Index', 'X_Coordinate', 'Y_Coordinate'])
                
                # Write anchor points
                for idx, (x, y) in enumerate(anchor_points):
                    writer.writerow([idx, f'{x:.6f}', f'{y:.6f}'])
                
        except Exception as e:
            raise RuntimeError(f"Error exporting anchor points CSV: {str(e)}")