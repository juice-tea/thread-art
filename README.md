# Thread Art Generator

A PySide6 GUI application for generating thread art paths from anchor points and target images.

## Features

- **DXF Import**: Load anchor point positions from DXF files
- **Image Processing**: Process target images for optimal thread art generation
- **Thread Path Generation**: Generate optimal threading paths using advanced algorithms
- **CSV Export**: Export thread paths as CSV files for manufacturing
- **Simulation**: Generate realistic previews of the final thread art
- **User-friendly GUI**: Intuitive interface built with PySide6

## Installation

1. Clone the repository:
```bash
git clone https://github.com/juice-tea/thread-art.git
cd thread-art
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### 1. Load Anchor Points
- Click "Load DXF (Anchor Points)" to load anchor point positions from a DXF file
- Or use the default circular anchor pattern (256 points)
- Supported DXF entities: POINT, CIRCLE, LINE, POLYLINE

### 2. Load Target Image
- Click "Load Image" to select your target image
- Supported formats: PNG, JPG, JPEG, BMP, TIFF
- Image will be automatically preprocessed for optimal thread art generation

### 3. Configure Parameters
- **Max Lines**: Maximum number of thread lines (100-10000)
- **Line Weight**: Darkness factor for each thread line (1.0-100.0)

### 4. Generate Thread Art
- Click "Generate Thread Art" to start the generation process
- The algorithm will find the optimal path between anchor points
- Progress will be shown in the progress bar

### 5. Export Results
- **Export Path to CSV**: Save the threading sequence as a CSV file
- **Export Simulation Image**: Save the thread art preview as an image

## File Formats

### DXF Files
The application reads anchor points from DXF files. Supported entities:
- `POINT`: Direct anchor points
- `CIRCLE`: Center points used as anchors
- `LINE`: Both endpoints used as anchors  
- `POLYLINE`/`LWPOLYLINE`: All vertices used as anchors

### CSV Output
The exported CSV contains:
- Step number
- Anchor point index
- X and Y coordinates (normalized 0-1)
- Metadata about generation parameters

### Images
- Input: PNG, JPG, JPEG, BMP, TIFF
- Output: PNG simulation images

## Algorithm

The thread art generation uses a greedy algorithm that:
1. Starts from an initial anchor point
2. Evaluates all possible next connections
3. Selects the line that best matches the target image darkness
4. Updates the working image to simulate thread placement
5. Repeats until the maximum line count is reached

## Testing

Run the test suite to verify installation:
```bash
python test_complete.py
```

Create test files for experimentation:
```bash
python create_test_files.py
```

## System Requirements

- Python 3.8+
- PySide6 (Qt6)
- NumPy
- OpenCV
- ezdxf
- Pillow
- SciPy
- Matplotlib

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests. 
