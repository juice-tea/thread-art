"""
Image display widget for showing images in the GUI.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
import numpy as np

from ..core.image_processor import ImageProcessor


class ImageDisplayWidget(QWidget):
    """Widget for displaying images with zoom and scroll capabilities."""
    
    def __init__(self, title: str = "Image"):
        super().__init__()
        self.title = title
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the widget UI."""
        layout = QVBoxLayout(self)
        
        # Title label
        self.title_label = QLabel(self.title)
        font = QFont()
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Scroll area for image
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setText("No image loaded")
        
        self.scroll_area.setWidget(self.image_label)
        layout.addWidget(self.scroll_area)
        
        # Info label
        self.info_label = QLabel("Size: -")
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)
    
    def set_image(self, image: np.ndarray):
        """
        Set the image to display.
        
        Args:
            image: Image array (grayscale or color)
        """
        try:
            # Convert numpy array to QImage
            qimage = ImageProcessor.array_to_qimage(image)
            
            # Convert to QPixmap and display
            pixmap = QPixmap.fromImage(qimage)
            self.image_label.setPixmap(pixmap)
            self.image_label.resize(pixmap.size())
            
            # Update info
            height, width = image.shape[:2]
            self.info_label.setText(f"Size: {width} x {height}")
            
        except Exception as e:
            self.image_label.setText(f"Error displaying image: {str(e)}")
            self.info_label.setText("Size: -")
    
    def clear_image(self):
        """Clear the displayed image."""
        self.image_label.clear()
        self.image_label.setText("No image loaded")
        self.info_label.setText("Size: -")