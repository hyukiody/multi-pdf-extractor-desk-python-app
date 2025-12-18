# Multi-PDF Extractor Desktop Application

A Python-based desktop application for extracting and processing data from multiple PDF files, specifically designed for utility bill analysis. The application features a user-friendly GUI built with tkinter and provides data visualization capabilities.

## Features

- **Multi-PDF Processing**: Process multiple PDF files in batch mode
- **Data Extraction**: Automatically extract structured data from utility bills (matriculation numbers, values, cities, consumption)
- **CSV Export**: Generate CSV files with extracted data for further analysis
- **Data Visualization**: Create summary tables with aggregated data by city
- **Desktop GUI**: User-friendly interface built with tkinter
- **Cross-Platform**: Works on Windows and Linux systems

## Technologies Used

- **Python**: Core programming language
- **pdfplumber**: PDF text extraction
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical operations and data processing
- **matplotlib**: Data visualization and table generation
- **tkinter**: Desktop GUI framework

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/hyukiody/multi-pdf-extractor-desk-python-app.git
cd multi-pdf-extractor-desk-python-app
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running from Source

Run the main application:
```bash
python multi-pdf-extractor-desk-app.py
```

### Using the Pre-compiled Executable

A pre-compiled executable version is available for download:
https://drive.google.com/file/d/198q4DcTuSkHrOmeepPAljTLt1IzMcTyC/view?usp=drive_link

**Important Notes:**

- **Windows users**: Active antivirus software may flag the executable as suspicious (common with PyInstaller-compiled apps). You may need to:
  - Temporarily disable your antivirus
  - Add the executable to your antivirus exception list
  - Allow execution when prompted

- **Linux users**: Grant execution permissions using:
```bash
chmod +x "filename"
```

*Note: The executable is clean and safe. PyInstaller-compiled applications are sometimes flagged by antivirus software due to the packaging method, not because of malicious content.*

### Application Workflow

1. **Launch the application**: Run the Python script or executable
2. **Select PDF files**: Click "Selecionar Arquivos PDF" to choose one or more PDF files
3. **Confirm processing**: Click "Confirmar Processamento" to start extraction
4. **Review results**: The application creates a folder for each PDF with:
   - `output.csv`: Extracted data in CSV format
   - `tabela.png`: Visual summary table grouped by city

## Project Structure

```
multi-pdf-extractor-desk-python-app/
├── multi-pdf-extractor-desk-app.py  # Main GUI application
├── my_script.py                      # Core data extraction functions
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation
└── upx-package/                      # UPX compression tool (for executable building)
```

## Contributing

Contributions are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests with improvements
- Suggest enhancements to the extraction algorithms

## Support

If you encounter any problems with the application or executable file, please open an issue on GitHub. I'll be happy to help!

## License

This project is available for educational and professional use.
