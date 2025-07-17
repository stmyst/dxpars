# DXPARS

A fast and simple Python library for analyzing and parsing Microsoft Word (DOCX) files, written in pure Python. DXPARS provides an intuitive API for extracting text content, working with formatting, tables, and converting documents to plain text.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)

## Key Features

* **Zero Dependencies**: Written in pure Python with no external dependencies
* **Format Support**: Extract and work with document formatting styles (headings, alignment, etc.)
* **Table Handling**: Parse and extract data from complex table structures
* **Text Conversion**: Easy conversion to plain text files
* **Performance**: Fast parsing of large documents
* **Simple API**: Intuitive interface for document manipulation

## Installation 

DXPARS requires Python 3.9 or higher. You can install it using pip:

```bash
pip install dxpars
```

Or install from source:

```bash
git clone https://github.com/stmyst/dxpars.git
cd dxpars
pip install .
```

## Usage

### Basic Usage

```python
from dxpars.document import Document

# Load a document
document = Document('path_to_file.docx')

# Get full document text
print(document.text)

# Save as plain text
document.to_txt('output.txt')
```

### Working with Formatting

```python
# Extract headings
for paragraph in document.paragraphs:
    if paragraph.pstyle is not None:
        if 'Heading' in paragraph.pstyle:
            print(f'Heading: {paragraph.text}')

# Get formatted data
for paragraph in document.paragraphs:
    for run in paragraph.parts:
        if run.bold:
            print(f'Bold text: {run.text}')
```

### Working with Tables

```python
for table in document.tables:
    # Display table structure
    print(table.show)  
    
    # Get all table text
    print(table.text)
    
    # Access cells by position
    cell = table.parts[0].parts[0]
    print(f'First cell: {cell.text}')
```

For more examples check out the [examples](examples/) directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
