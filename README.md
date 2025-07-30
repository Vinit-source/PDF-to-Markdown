# PDF to Markdown Converter with LLM Enhancement

A sophisticated MCP (Model Context Protocol) server that converts PDF files to Markdown format while intelligently preserving document structure, formatting, links, lists, headings, and images using advanced LLM-enhanced analysis.

## Features

### 🧠 Smart Structure Detection
- **LLM-Enhanced Analysis**: Uses Large Language Models to intelligently identify document hierarchy beyond simple heuristics
- **Semantic Understanding**: Recognizes the meaning and context of text blocks for accurate classification
- **Advanced Pattern Recognition**: Detects complex list structures, nested formatting, and document sections
- **Fallback Heuristics**: Robust font-size and pattern-based analysis when LLM is unavailable

### 📄 Format Preservation
- **Heading Hierarchy**: Maintains proper markdown heading levels (# ## ### ####)
- **Lists**: Preserves bullet points, numbered lists, and nested structures
- **Images**: Extracts images and creates proper markdown references
- **Links**: Maintains internal and external link references
- **Tables**: Handles table structures and formatting
- **Styling**: Preserves bold, italic, and other text formatting

### 🔧 MCP Server Integration
- **Three Main Tools**:
  - `convert_pdf_to_markdown`: Full PDF to Markdown conversion
  - `convert_pdf_from_base64`: Convert base64-encoded PDFs
  - `analyze_pdf_structure`: Analyze document structure without full conversion
- **Flexible Configuration**: Optional LLM integration, customizable output, image extraction control
- **Error Handling**: Robust error handling with meaningful feedback

## Installation

```bash
# Clone or download the project
cd pdf_to_markdown

# Install dependencies
pip install -r requirements.txt
```

## Usage

### As a Standalone Script

```bash
# Basic conversion
python pdf_to_markdown.py document.pdf

# With custom output directory
python pdf_to_markdown.py document.pdf -o /path/to/output

# With LLM enhancement
python pdf_to_markdown.py document.pdf \
  --llm-api-url "https://api.openai.com/v1/chat/completions" \
  --llm-api-key "your-api-key"

# Skip image extraction
python pdf_to_markdown.py document.pdf --no-images
```

### As an MCP Server

```bash
# Start the MCP server
python mcp_server.py
```

The server exposes three tools via the Model Context Protocol:

#### 1. convert_pdf_to_markdown
Converts a PDF file to Markdown format with intelligent structure detection.

**Parameters:**
- `pdf_path` (required): Path to the PDF file
- `output_dir` (optional): Output directory for results
- `output_name` (optional): Custom name for the markdown file
- `extract_images` (optional): Whether to extract images (default: true)
- `llm_api_url` (optional): LLM API endpoint for enhanced analysis
- `llm_api_key` (optional): API key for LLM service

#### 2. convert_pdf_from_base64
Converts a base64-encoded PDF to Markdown format.

**Parameters:**
- `pdf_base64` (required): Base64-encoded PDF content
- `filename` (required): Original filename for naming output
- `output_dir` (optional): Output directory
- `extract_images` (optional): Whether to extract images (default: true)
- `llm_api_url` (optional): LLM API endpoint
- `llm_api_key` (optional): API key for LLM service

#### 3. analyze_pdf_structure
Analyzes PDF structure without full conversion, useful for understanding document layout.

**Parameters:**
- `pdf_path` (required): Path to the PDF file
- `llm_api_url` (optional): LLM API endpoint for enhanced analysis
- `llm_api_key` (optional): API key for LLM service

### Python API

```python
from pdf_to_markdown import PDFToMarkdownConverter

# Create converter with LLM enhancement
converter = PDFToMarkdownConverter(
    pdf_path="document.pdf",
    output_dir="output",
    extract_images=True,
    llm_api_url="https://api.openai.com/v1/chat/completions",
    llm_api_key="your-api-key"
)

# Convert PDF
output_path = converter.convert()
print(f"Conversion completed: {output_path}")
```

## Smart Algorithm Details

### LLM-Enhanced Structure Detection

The converter uses a multi-stage approach for intelligent document analysis:

1. **Text Extraction with Metadata**: Extracts text along with font information, positioning, and formatting details
2. **LLM Analysis**: Sends structured text blocks to an LLM for semantic analysis and classification
3. **Structure Mapping**: Maps LLM classifications to appropriate markdown elements
4. **Post-Processing**: Applies additional formatting rules and cleanup

### Fallback Heuristics

When LLM is not available, the system uses sophisticated heuristics:

- **Font Size Analysis**: Larger fonts typically indicate headings
- **Pattern Recognition**: Detects list markers, numbering patterns
- **Positional Analysis**: Uses text positioning for structure hints
- **Content Patterns**: Recognizes common document structures

### Supported Document Elements

- **Headings**: H1-H6 based on font size and LLM analysis
- **Paragraphs**: Regular text content with proper spacing
- **Lists**: Bullet points, numbered lists, nested structures
- **Images**: Extracted as PNG files with markdown references
- **Tables**: Basic table structure preservation
- **Links**: Internal and external link maintenance
- **Formatting**: Bold, italic, and other text styles

## Configuration

### LLM Integration

The system supports any OpenAI-compatible API:

```python
# Example configurations
llm_configs = {
    "openai": {
        "url": "https://api.openai.com/v1/chat/completions",
        "key": "sk-..."
    },
    "anthropic": {
        "url": "https://api.anthropic.com/v1/messages",
        "key": "sk-ant-..."
    },
    "local": {
        "url": "http://localhost:1234/v1/chat/completions",
        "key": "not-needed"
    }
}
```

### Output Customization

- **Directory Structure**: Automatically creates organized output directories
- **Image Handling**: Configurable image extraction and referencing
- **Naming Conventions**: Flexible file naming with hash-based deduplication
- **Format Options**: Clean markdown with proper spacing and hierarchy

## Error Handling

The system includes comprehensive error handling:

- **File Validation**: Checks for valid PDF files and permissions
- **Network Resilience**: Handles LLM API failures gracefully
- **Memory Management**: Efficient handling of large PDFs
- **Corruption Recovery**: Attempts to process partially corrupted PDFs

## Examples

### Basic Document Conversion

```python
# Convert a simple document
converter = PDFToMarkdownConverter("report.pdf")
output = converter.convert()
```

### Advanced Document with LLM

```python
# Convert with enhanced structure detection
converter = PDFToMarkdownConverter(
    pdf_path="complex_document.pdf",
    llm_api_url="https://api.openai.com/v1/chat/completions",
    llm_api_key="your-key"
)
output = converter.convert("enhanced_output.md")
```

### Structure Analysis Only

```python
# Analyze document structure without full conversion
converter = PDFToMarkdownConverter("document.pdf")
converter.open_pdf()
blocks = converter.extract_text_with_formatting(converter.doc[0])
structure = converter.analyze_structure_with_llm(blocks)
print(json.dumps(structure, indent=2))
```

## Dependencies

- `pymupdf>=1.23.0` - PDF processing
- `Pillow>=10.0.0` - Image handling
- `requests>=2.31.0` - HTTP requests for LLM APIs
- `mcp>=1.0.0` - Model Context Protocol server
- `pydantic>=2.0.0` - Data validation

## License

This project is available under the terms specified in the LICENSE file.

## Contributing

Contributions are welcome! Please ensure:

1. Code follows Python best practices
2. New features include appropriate tests
3. Documentation is updated for new functionality
4. LLM integration remains optional for accessibility

## Troubleshooting

### Common Issues

**PyMuPDF Installation**: On some systems, you may need to install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install libmupdf-dev

# macOS with Homebrew
brew install mupdf-tools
```

**Memory Issues**: For large PDFs, consider processing in chunks or using a machine with more RAM.

**LLM API Errors**: The system gracefully falls back to heuristic analysis if LLM APIs are unavailable.

**Image Extraction**: Some PDFs have embedded images that may not extract cleanly. The system handles these cases gracefully.
