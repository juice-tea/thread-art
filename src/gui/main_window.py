"""
Main window for the Thread Art Generator application.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QProgressBar,
    QSpinBox, QDoubleSpinBox, QGroupBox, QScrollArea, QSplitter,
    QTextEdit, QStatusBar, QMenuBar, QMenu
)
from PySide6.QtCore import Qt, QThread, QTimer, QDateTime
from PySide6.QtGui import QPixmap, QAction, QFont
import os
from typing import Optional, List, Tuple

from ..core.dxf_processor import DXFProcessor
from ..core.image_processor import ImageProcessor
from ..core.thread_art import ThreadArtGenerator
from ..utils.csv_exporter import CSVExporter
from ..utils.progress_tracker import ProgressTracker
from .image_display import ImageDisplayWidget
from .generation_worker import ThreadArtWorker


class ThreadArtMainWindow(QMainWindow):
    """Main window for the Thread Art Generator application."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thread Art Generator")
        self.setMinimumSize(1200, 800)
        
        # Initialize data
        self.anchor_points: Optional[List[Tuple[float, float]]] = None
        self.input_image: Optional[str] = None
        self.processed_image = None
        self.generated_path: Optional[List[int]] = None
        self.simulation_image = None
        
        # Initialize worker thread
        self.worker_thread: Optional[QThread] = None
        self.worker: Optional[ThreadArtWorker] = None
        
        # Set up UI
        self._setup_ui()
        self._setup_menus()
        self._setup_status_bar()
        self._connect_signals()
        
        # Load default circular anchors
        self._load_default_anchors()
    
    def _setup_ui(self):
        """Set up the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel for controls
        left_panel = self._create_control_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Right panel for image display
        right_panel = self._create_display_panel()
        main_layout.addWidget(right_panel, 3)
    
    def _create_control_panel(self) -> QWidget:
        """Create the left control panel."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # File input section
        file_group = QGroupBox("Input Files")
        file_layout = QVBoxLayout(file_group)
        
        # DXF file input
        dxf_layout = QHBoxLayout()
        self.dxf_label = QLabel("No DXF file selected")
        self.dxf_button = QPushButton("Load DXF (Anchor Points)")
        dxf_layout.addWidget(self.dxf_button)
        dxf_layout.addWidget(self.dxf_label, 1)
        file_layout.addLayout(dxf_layout)
        
        # Image file input
        image_layout = QHBoxLayout()
        self.image_label = QLabel("No image selected")
        self.image_button = QPushButton("Load Image")
        image_layout.addWidget(self.image_button)
        image_layout.addWidget(self.image_label, 1)
        file_layout.addLayout(image_layout)
        
        layout.addWidget(file_group)
        
        # Generation parameters
        params_group = QGroupBox("Generation Parameters")
        params_layout = QGridLayout(params_group)
        
        params_layout.addWidget(QLabel("Max Lines:"), 0, 0)
        self.max_lines_spin = QSpinBox()
        self.max_lines_spin.setRange(100, 10000)
        self.max_lines_spin.setValue(3000)
        params_layout.addWidget(self.max_lines_spin, 0, 1)
        
        params_layout.addWidget(QLabel("Line Weight:"), 1, 0)
        self.line_weight_spin = QDoubleSpinBox()
        self.line_weight_spin.setRange(1.0, 100.0)
        self.line_weight_spin.setValue(25.0)
        params_layout.addWidget(self.line_weight_spin, 1, 1)
        
        layout.addWidget(params_group)
        
        # Generation controls
        gen_group = QGroupBox("Generation")
        gen_layout = QVBoxLayout(gen_group)
        
        self.generate_button = QPushButton("Generate Thread Art")
        self.generate_button.setEnabled(False)
        gen_layout.addWidget(self.generate_button)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        gen_layout.addWidget(self.progress_bar)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setVisible(False)
        gen_layout.addWidget(self.cancel_button)
        
        layout.addWidget(gen_group)
        
        # Export controls
        export_group = QGroupBox("Export")
        export_layout = QVBoxLayout(export_group)
        
        self.export_csv_button = QPushButton("Export Path to CSV")
        self.export_csv_button.setEnabled(False)
        export_layout.addWidget(self.export_csv_button)
        
        self.export_image_button = QPushButton("Export Simulation Image")
        self.export_image_button.setEnabled(False)
        export_layout.addWidget(self.export_image_button)
        
        layout.addWidget(export_group)
        
        # Status text
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout(status_group)
        
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(100)
        self.status_text.setReadOnly(True)
        status_layout.addWidget(self.status_text)
        
        layout.addWidget(status_group)
        
        layout.addStretch()
        
        return panel
    
    def _create_display_panel(self) -> QWidget:
        """Create the right display panel."""
        splitter = QSplitter(Qt.Horizontal)
        
        # Original image display
        self.original_display = ImageDisplayWidget("Original Image")
        splitter.addWidget(self.original_display)
        
        # Simulation display
        self.simulation_display = ImageDisplayWidget("Thread Art Simulation")
        splitter.addWidget(self.simulation_display)
        
        splitter.setSizes([1, 1])
        return splitter
    
    def _setup_menus(self):
        """Set up the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        open_dxf_action = QAction("Open DXF...", self)
        open_dxf_action.triggered.connect(self._load_dxf_file)
        file_menu.addAction(open_dxf_action)
        
        open_image_action = QAction("Open Image...", self)
        open_image_action.triggered.connect(self._load_image_file)
        file_menu.addAction(open_image_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _setup_status_bar(self):
        """Set up the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _connect_signals(self):
        """Connect UI signals to slots."""
        self.dxf_button.clicked.connect(self._load_dxf_file)
        self.image_button.clicked.connect(self._load_image_file)
        self.generate_button.clicked.connect(self._start_generation)
        self.cancel_button.clicked.connect(self._cancel_generation)
        self.export_csv_button.clicked.connect(self._export_csv)
        self.export_image_button.clicked.connect(self._export_image)
    
    def _load_default_anchors(self):
        """Load default circular anchor points."""
        try:
            self.anchor_points = DXFProcessor.create_circular_anchors(256)
            self.dxf_label.setText("Default circular anchors (256 points)")
            self._update_status("Default circular anchor points loaded")
            self._check_ready_to_generate()
        except Exception as e:
            self._show_error(f"Error creating default anchors: {str(e)}")
    
    def _load_dxf_file(self):
        """Load DXF file for anchor points."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open DXF File", "", "DXF Files (*.dxf);;All Files (*)"
        )
        
        if file_path:
            try:
                self.anchor_points = DXFProcessor.load_anchor_points(file_path)
                filename = os.path.basename(file_path)
                self.dxf_label.setText(f"{filename} ({len(self.anchor_points)} points)")
                self._update_status(f"Loaded {len(self.anchor_points)} anchor points from {filename}")
                self._check_ready_to_generate()
            except Exception as e:
                self._show_error(f"Error loading DXF file: {str(e)}")
    
    def _load_image_file(self):
        """Load image file for processing."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image File", "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff);;All Files (*)"
        )
        
        if file_path:
            try:
                self.processed_image = ImageProcessor.load_and_preprocess(file_path)
                self.input_image = file_path
                filename = os.path.basename(file_path)
                self.image_label.setText(filename)
                
                # Display the processed image
                self.original_display.set_image(self.processed_image)
                
                self._update_status(f"Loaded and processed image: {filename}")
                self._check_ready_to_generate()
            except Exception as e:
                self._show_error(f"Error loading image: {str(e)}")
    
    def _check_ready_to_generate(self):
        """Check if ready to generate thread art."""
        ready = self.anchor_points is not None and self.processed_image is not None
        self.generate_button.setEnabled(ready)
    
    def _start_generation(self):
        """Start thread art generation in a separate thread."""
        if not self.anchor_points or self.processed_image is None:
            return
        
        # Disable controls
        self.generate_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.cancel_button.setVisible(True)
        
        # Create worker thread
        self.worker_thread = QThread()
        self.worker = ThreadArtWorker(
            self.anchor_points,
            self.processed_image,
            self.max_lines_spin.value(),
            self.line_weight_spin.value()
        )
        self.worker.moveToThread(self.worker_thread)
        
        # Connect signals
        self.worker_thread.started.connect(self.worker.run)
        self.worker.progress_updated.connect(self._update_progress)
        self.worker.finished.connect(self._generation_finished)
        self.worker.error_occurred.connect(self._generation_error)
        
        # Start the thread
        self.worker_thread.start()
        self._update_status("Generating thread art...")
    
    def _cancel_generation(self):
        """Cancel the current generation."""
        if self.worker:
            self.worker.cancel()
    
    def _update_progress(self, value: int, message: str):
        """Update the progress bar."""
        self.progress_bar.setValue(value)
        if message:
            self.status_bar.showMessage(message)
    
    def _generation_finished(self, path: List[int], simulation: any):
        """Handle generation completion."""
        self.generated_path = path
        self.simulation_image = simulation
        
        # Display the simulation
        self.simulation_display.set_image(simulation)
        
        # Enable export buttons
        self.export_csv_button.setEnabled(True)
        self.export_image_button.setEnabled(True)
        
        # Reset UI
        self._reset_generation_ui()
        self._update_status(f"Thread art generated successfully! Path length: {len(path)} lines")
    
    def _generation_error(self, error_message: str):
        """Handle generation error."""
        self._show_error(f"Generation error: {error_message}")
        self._reset_generation_ui()
    
    def _reset_generation_ui(self):
        """Reset the generation UI to normal state."""
        self.generate_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.cancel_button.setVisible(False)
        
        if self.worker_thread:
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.worker_thread = None
            self.worker = None
    
    def _export_csv(self):
        """Export the generated path to CSV."""
        if not self.generated_path or not self.anchor_points:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV File", "thread_art_path.csv", "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            try:
                metadata = {
                    "Max Lines": self.max_lines_spin.value(),
                    "Line Weight": self.line_weight_spin.value(),
                    "Anchor Points": len(self.anchor_points),
                    "Path Length": len(self.generated_path)
                }
                
                CSVExporter.export_path(
                    self.generated_path, 
                    self.anchor_points, 
                    file_path, 
                    metadata
                )
                
                self._update_status(f"Path exported to: {os.path.basename(file_path)}")
            except Exception as e:
                self._show_error(f"Error exporting CSV: {str(e)}")
    
    def _export_image(self):
        """Export the simulation image."""
        if self.simulation_image is None:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Simulation Image", "thread_art_simulation.png", 
            "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)"
        )
        
        if file_path:
            try:
                ImageProcessor.save_image(self.simulation_image, file_path)
                self._update_status(f"Simulation exported to: {os.path.basename(file_path)}")
            except Exception as e:
                self._show_error(f"Error exporting image: {str(e)}")
    
    def _update_status(self, message: str):
        """Update the status display."""
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        self.status_text.append(f"[{timestamp}] {message}")
        self.status_bar.showMessage(message)
    
    def _show_error(self, message: str):
        """Show an error message."""
        QMessageBox.critical(self, "Error", message)
        self._update_status(f"ERROR: {message}")
    
    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self, "About Thread Art Generator",
            "Thread Art Generator v1.0\n\n"
            "Generate thread art paths from anchor points and target images.\n\n"
            "Features:\n"
            "• Load DXF files for anchor point positions\n"
            "• Process target images for thread art generation\n"
            "• Export paths as CSV files\n"
            "• Generate simulation images\n\n"
            "Copyright (c) 2025"
        )