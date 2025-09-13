"""
Progress tracking and status reporting utilities.
"""

from PySide6.QtCore import QObject, Signal
from typing import Optional, Callable


class ProgressTracker(QObject):
    """Tracks and reports progress for long-running operations."""
    
    # Signal emitted when progress is updated (value, message)
    progress_updated = Signal(int, str)
    # Signal emitted when operation is finished
    finished = Signal()
    # Signal emitted when operation encounters an error
    error_occurred = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._current_progress = 0
        self._max_progress = 100
        self._is_cancelled = False
    
    def set_max_progress(self, max_value: int):
        """Set the maximum progress value."""
        self._max_progress = max_value
    
    def update_progress(self, value: int, message: str = ""):
        """Update the current progress."""
        self._current_progress = value
        percentage = int((value / self._max_progress) * 100) if self._max_progress > 0 else 0
        self.progress_updated.emit(percentage, message)
    
    def cancel(self):
        """Cancel the current operation."""
        self._is_cancelled = True
    
    def is_cancelled(self) -> bool:
        """Check if the operation has been cancelled."""
        return self._is_cancelled
    
    def reset(self):
        """Reset the progress tracker."""
        self._current_progress = 0
        self._is_cancelled = False
    
    def report_error(self, error_message: str):
        """Report an error."""
        self.error_occurred.emit(error_message)
    
    def report_finished(self):
        """Report that the operation is finished."""
        self.finished.emit()