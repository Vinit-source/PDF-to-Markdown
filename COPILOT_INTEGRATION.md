# GitHub Copilot Chat MCP Integration Guide

This guide explains how to integrate the PDF to Markdown MCP server with GitHub Copilot Chat in VS Code.

## 🚀 Quick Setup

1. **Run the setup script:**
   ```bash
   ./setup_mcp_integration.sh
   ```

2. **Restart VS Code** to load the new MCP server configuration

3. **Open GitHub Copilot Chat** and start using the PDF conversion tools!

## 🔧 Manual Configuration

If you prefer to set up manually or need to troubleshoot:

### VS Code Settings

The MCP server is configured in `.vscode/settings.json`:

```json
{
  "github.copilot.chat.mcp.servers": {
    "pdf-to-markdown": {
      "command": "python",
      "args": ["pdf_to_markdown/mcp_server.py"],
      "cwd": "/Users/vinitgore/Documents/Learnings/JS DOM Template",
      "env": {},
      "description": "PDF to Markdown Converter with LLM Enhancement",
      "capabilities": ["tools"]
    }
  },
  "github.copilot.chat.mcp.enabled": true
}
```

### Dependencies

Ensure all Python dependencies are installed:

```bash
cd pdf_to_markdown
source venv/bin/activate  # if using virtual environment
pip install -r requirements.txt
```

## 💬 Using with GitHub Copilot Chat

Once configured, you can use these tools directly in GitHub Copilot Chat:

### Available Tools

1. **convert_pdf_to_markdown**
   - Convert PDF files to Markdown with smart structure detection
   - Supports LLM enhancement for better structure recognition
   - Extracts images and preserves formatting

2. **convert_pdf_from_base64**
   - Convert base64-encoded PDF content to Markdown
   - Useful for handling PDF data from web applications

3. **analyze_pdf_structure**
   - Analyze PDF structure without full conversion
   - Get document hierarchy and metadata

### Example Chat Commands

```
@pdf-to-markdown Convert this PDF to markdown: /path/to/document.pdf

@pdf-to-markdown Analyze the structure of /path/to/research-paper.pdf

@pdf-to-markdown Convert this PDF with LLM enhancement using OpenAI API

@pdf-to-markdown Extract images from this PDF and convert to markdown
```

### Advanced Usage

**With LLM Enhancement:**
```
Convert /path/to/complex-document.pdf to markdown using LLM API at https://api.openai.com/v1/chat/completions with my API key for better structure detection
```

**Custom Output Directory:**
```
Convert /path/to/document.pdf to markdown and save in /path/to/output directory
```

**Without Image Extraction:**
```
Convert /path/to/document.pdf to markdown but skip image extraction
```

## 🔍 Verification

To verify the integration is working:

1. **Check MCP Server Status:**
   ```bash
   python pdf_to_markdown/mcp_server.py --help
   ```

2. **Test in VS Code:**
   - Open GitHub Copilot Chat
   - Type `@` and you should see `pdf-to-markdown` in the suggestions
   - The tools should be available for use

3. **Check Logs:**
   - VS Code Developer Tools Console will show MCP server communication
   - Use `Cmd+Shift+P` → "Developer: Toggle Developer Tools"

## 🛠 Troubleshooting

### Common Issues

**MCP Server Not Found:**
- Ensure VS Code settings are correctly configured
- Check that the Python path and script paths are correct
- Restart VS Code after configuration changes

**Python Dependencies Missing:**
- Run the setup script or install dependencies manually
- Ensure virtual environment is activated if using one

**Permission Issues:**
- Make sure the setup script is executable: `chmod +x setup_mcp_integration.sh`
- Check file permissions for the MCP server files

**LLM API Issues:**
- The system gracefully falls back to heuristic analysis if LLM APIs fail
- Verify API URL and key format for LLM services

### Debug Mode

To enable debug logging, modify the MCP server:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 🎯 Features Overview

- **Smart Structure Detection**: Uses LLM analysis for intelligent document hierarchy identification
- **Format Preservation**: Maintains headings, lists, images, links, and text formatting
- **Image Extraction**: Automatically extracts and references images
- **Flexible Configuration**: Optional LLM integration, customizable output
- **Robust Error Handling**: Graceful fallbacks and comprehensive error messages
- **GitHub Copilot Integration**: Seamless integration with VS Code's AI assistant

## 📝 Example Workflows

### Research Paper Conversion
1. Ask Copilot: "Convert this research paper to markdown: /path/to/paper.pdf"
2. Copilot uses the MCP server to convert with structure detection
3. Get clean markdown with proper headings, citations, and references

### Document Analysis
1. Ask Copilot: "What's the structure of this document: /path/to/doc.pdf"
2. Get detailed analysis of document hierarchy and sections
3. Use insights to better understand document organization

### Batch Processing
1. Ask Copilot to convert multiple PDFs in a directory
2. Use the tools programmatically through Chat commands
3. Get consistent markdown output with preserved formatting

The integration is now complete and ready for use with GitHub Copilot Chat!