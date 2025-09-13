"""
Worker thread for thread art generation.
"""

from PySide6.QtCore import QObject, Signal
from typing import List, Tuple
import numpy as np

from ..core.thread_art import ThreadArtGenerator


class ThreadArtWorker(QObject):
    """Worker for generating thread art in a separate thread."""
    
    # Signals
    progress_updated = Signal(int, str)
    finished = Signal(list, object)  # path, simulation_image
    error_occurred = Signal(str)
    
    def __init__(self, anchor_points: List[Tuple[float, float]], 
                 image: np.ndarray, max_lines: int, line_weight: float):
        super().__init__()
        self.anchor_points = anchor_points
        self.image = image
        self.max_lines = max_lines
        self.line_weight = line_weight
        self._cancelled = False
    
    def run(self):
        """Run the thread art generation."""
        try:
            self.progress_updated.emit(0, "Initializing thread art generator...")
            
            # Create generator
            generator = ThreadArtGenerator(self.anchor_points, self.image)
            
            self.progress_updated.emit(10, "Generating thread path...")
            
            # Generate path with progress tracking
            path = self._generate_path_with_progress(generator)
            
            if self._cancelled:
                return
            
            self.progress_updated.emit(80, "Creating simulation...")
            
            # Generate simulation
            simulation = generator.generate_simulation(path)
            
            self.progress_updated.emit(100, "Generation complete!")
            
            # Emit results
            self.finished.emit(path, simulation)
            
        except Exception as e:
            self.error_occurred.emit(str(e))
    
    def _generate_path_with_progress(self, generator: ThreadArtGenerator) -> List[int]:
        """Generate path with progress updates."""
        # This is a simplified version - in a real implementation,
        # you'd want to modify the ThreadArtGenerator to support progress callbacks
        path = generator.generate_path(self.max_lines, self.line_weight)
        return path
    
    def cancel(self):
        """Cancel the generation."""
        self._cancelled = True