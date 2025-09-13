"""
Image processing utilities for thread art generation.
"""

import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Optional


class ImageProcessor:
    """Processes images for thread art generation."""
    
    @staticmethod
    def load_and_preprocess(file_path: str, target_size: Tuple[int, int] = (800, 600)) -> np.ndarray:
        """
        Load and preprocess an image for thread art generation.
        
        Args:
            file_path: Path to the image file
            target_size: Target size (width, height) for the processed image
            
        Returns:
            Preprocessed grayscale image as numpy array
        """
        try:
            # Load image using PIL for better format support
            pil_image = Image.open(file_path)
            
            # Convert to RGB if necessary
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Convert to numpy array
            image = np.array(pil_image)
            
            # Convert to OpenCV format (BGR)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Resize to target size
            image = cv2.resize(image, target_size)
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply preprocessing for better thread art results
            processed = ImageProcessor._enhance_for_thread_art(gray)
            
            return processed
            
        except Exception as e:
            raise RuntimeError(f"Error processing image: {str(e)}")
    
    @staticmethod
    def _enhance_for_thread_art(image: np.ndarray) -> np.ndarray:
        """
        Apply enhancements to make the image more suitable for thread art.
        
        Args:
            image: Grayscale image
            
        Returns:
            Enhanced image
        """
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(image, (3, 3), 0)
        
        # Enhance contrast using CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(blurred)
        
        # Apply edge enhancement to preserve important features
        edges = cv2.Canny(enhanced, 50, 150)
        
        # Combine original with edge information
        result = cv2.addWeighted(enhanced, 0.8, edges, 0.2, 0)
        
        return result
    
    @staticmethod
    def save_image(image: np.ndarray, file_path: str):
        """
        Save an image to file.
        
        Args:
            image: Image array to save
            file_path: Output file path
        """
        try:
            cv2.imwrite(file_path, image)
        except Exception as e:
            raise RuntimeError(f"Error saving image: {str(e)}")
    
    @staticmethod
    def array_to_qimage(image: np.ndarray):
        """
        Convert numpy array to QImage for display in Qt widgets.
        
        Args:
            image: Image array (grayscale or BGR)
            
        Returns:
            QImage object
        """
        from PySide6.QtGui import QImage
        
        if len(image.shape) == 2:  # Grayscale
            height, width = image.shape
            bytes_per_line = width
            return QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        elif len(image.shape) == 3:  # Color
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            # Convert BGR to RGB for Qt
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            return QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        else:
            raise ValueError("Unsupported image format")