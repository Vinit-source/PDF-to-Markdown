# GitHub Copilot Chat MCP Integration Guide

This guide explains how to integrate the PDF to Markdown MCP server with GitHub Copilot Chat in VS Code for seamless PDF document analysis and conversion.

## 🚀 Quick Setup

1. **Run the setup script:**
   ```bash
   chmod +x setup_mcp_integration.sh
   ./setup_mcp_integration.sh
   ```

2. **Restart VS Code** to load the new MCP server configuration

3. **Open GitHub Copilot Chat** and start converting PDFs to Markdown!

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
      "description": "PDF to Markdown Converter with GitHub Copilot Integration",
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
pip install -r requirements.txt
```

## 💬 Using with GitHub Copilot Chat

Once configured, you can use these tools directly in GitHub Copilot Chat:

### Available Tools

1. **convert_pdf_to_markdown**
   - Convert PDF files to Markdown with intelligent structure detection
   - Automatically analyzes document hierarchy and formatting
   - Extracts images and preserves layout

2. **convert_pdf_from_base64**
   - Convert base64-encoded PDF content to Markdown
   - Useful for handling PDF data from web applications or APIs

3. **analyze_pdf_structure**
   - Analyze PDF structure and metadata without full conversion
   - Get document hierarchy, section analysis, and content overview

### Example Chat Commands

**Basic Conversion:**
```
Convert the JavaScript curriculum PDF to markdown
```

**Using File Path:**
```
Convert JavaScript-DOM-challenges-TODO-application/v3/Outline.pdf to markdown
```

**Structure Analysis:**
```
Analyze the structure of the Outline.pdf file
```

**With Custom Output:**
```
Convert Outline.pdf to markdown and save it in the docs folder
```

### Advanced Usage Examples

**Educational Content Processing:**
```
Convert the JavaScript fundamentals PDF to markdown, preserving the curriculum structure and code examples
```

**Research Document Analysis:**
```
Analyze the structure of this research paper and then convert it to markdown with proper academic formatting
```

**Multi-document Processing:**
```
Convert all PDFs in the JavaScript-DOM-challenges-TODO-application folder to markdown
```

## 🎯 Sample Workflow with Outline.pdf

The workspace includes a sample PDF (`JavaScript-DOM-challenges-TODO-application/v3/Outline.pdf`) that you can use to test the integration:

1. **Quick Test:**
   ```
   Convert the Outline.pdf to see how it works
   ```

2. **Detailed Analysis:**
   ```
   First analyze the structure of Outline.pdf, then convert it to markdown with enhanced formatting
   ```

3. **Curriculum Processing:**
   ```
   Convert the JavaScript curriculum Outline.pdf to markdown, maintaining the educational structure and learning objectives
   ```

## 🔍 Verification Steps

### 1. Check MCP Server Status
Open VS Code Developer Tools (`Cmd+Option+I`) and look for MCP server logs.

### 2. Test in Copilot Chat
- Open GitHub Copilot Chat (`Cmd+Shift+I`)
- Type `@` and you should see `pdf-to-markdown` in the suggestions
- Try: `Convert Outline.pdf to markdown`

### 3. Verify File Processing
The converter should:
- ✅ Detect document structure automatically
- ✅ Preserve headings and formatting
- ✅ Extract and reference images
- ✅ Maintain links and references
- ✅ Generate clean markdown output

## 🛠 Troubleshooting

### Common Issues and Solutions

**MCP Server Not Available:**
```bash
# Check if the server starts correctly
python pdf_to_markdown/mcp_server.py --help
```

**Dependencies Missing:**
```bash
# Install required packages
pip install -r pdf_to_markdown/requirements.txt
```

**VS Code Integration Issues:**
1. Restart VS Code after configuration changes
2. Check `.vscode/settings.json` for correct paths
3. Verify MCP is enabled in Copilot settings

**PDF Processing Errors:**
- Ensure PDF files are not corrupted or password-protected
- Check file paths are correct and accessible
- Verify sufficient disk space for output files

### Debug Mode

Enable debug logging by modifying the MCP server configuration:

```json
{
  "github.copilot.chat.mcp.servers": {
    "pdf-to-markdown": {
      "command": "python",
      "args": ["pdf_to_markdown/mcp_server.py", "--debug"],
      // ...existing code...
    }
  }
}
```

## 📚 Features Overview

### Smart Document Analysis
- **Automatic Structure Detection**: Intelligently identifies headings, sections, and content hierarchy
- **Educational Content Recognition**: Specialized handling for curriculum and learning materials
- **Format Preservation**: Maintains original document formatting and layout

### Flexible Output Options
- **Customizable Output Directories**: Save converted files where you need them
- **Image Extraction**: Automatically extracts and references embedded images
- **Multiple Input Formats**: Support for various PDF types and encodings

### GitHub Copilot Integration
- **Seamless Chat Commands**: Natural language requests for PDF conversion
- **Context-Aware Processing**: Understands document type and adjusts processing accordingly
- **Batch Processing Support**: Handle multiple documents through chat interface

## 🎓 Educational Use Cases

### JavaScript Curriculum Processing
Perfect for converting educational PDFs like the included JavaScript fundamentals outline:
- Preserves learning objectives and curriculum structure
- Maintains code examples and technical formatting
- Creates navigable markdown for easy reference

### Research and Documentation
- Convert academic papers with proper citation formatting
- Maintain technical diagrams and figures
- Preserve complex document structures

### Content Management
- Batch convert document libraries
- Standardize formatting across document collections
- Create searchable markdown archives

## 🚀 Next Steps

1. **Test the Integration**: Use the sample Outline.pdf to verify everything works
2. **Explore Features**: Try different conversion options and output formats
3. **Customize Settings**: Adjust the MCP configuration for your specific needs
4. **Process Your Documents**: Start converting your PDF library to markdown

The integration is now optimized for GitHub Copilot Chat and ready for productive use!