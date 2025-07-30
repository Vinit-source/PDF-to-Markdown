# PDF to Markdown Converter

A comprehensive Python script that converts PDF files to Markdown format while preserving formatting, links, and images.

## Features

- **Text Formatting**: Preserves bold and italic text from PDF
- **Heading Detection**: Automatically detects headings based on font size
- **Link Extraction**: Extracts both external URLs and internal page links
- **Image Extraction**: Saves images as PNG files and references them in markdown
- **Document Structure**: Maintains document flow and adds page separators
- **Command Line Interface**: Easy-to-use CLI with various options

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pymupdf Pillow requests
```

## Usage

### Command Line Interface

Basic usage:
```bash
python pdf_to_markdown.py input.pdf
```

With options:
```bash
python pdf_to_markdown.py input.pdf -o ./output -n custom_name.md
```

Skip image extraction:
```bash
python pdf_to_markdown.py input.pdf --no-images
```

### Command Line Options

- `pdf_path`: Path to the input PDF file (required)
- `-o, --output`: Output directory (default: same as PDF file)
- `-n, --name`: Output filename (default: PDF name + .md)
- `--no-images`: Skip image extraction

### Python API

```python
from pdf_to_markdown import PDFToMarkdownConverter

# Basic conversion
converter = PDFToMarkdownConverter("document.pdf")
output_path = converter.convert()

# Advanced options
converter = PDFToMarkdownConverter(
    pdf_path="document.pdf",
    output_dir="./output",
    extract_images=True
)
output_path = converter.convert("custom_name.md")
```

## Output Structure

The converter creates:
- A markdown file with the converted content
- An `images/` directory (if images are extracted) containing PNG files
- Proper markdown formatting with headers, links, and image references

## Example Output

```markdown
# Document Title

## Page 1

This is **bold text** and this is *italic text*.

Here's a [link to example.com](https://example.com).

### Images

![Image](images/image_1_1_a1b2c3d4.png)
```

## Dependencies

- `pymupdf`: PDF processing and text extraction
- `Pillow`: Image processing
- `requests`: HTTP requests (for future enhancements)

## Limitations

- Complex layouts may not be perfectly preserved
- Table extraction is basic
- Some PDF features (annotations, forms) are not supported
- Image quality depends on the source PDF

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.# PDF-to-Markdown
