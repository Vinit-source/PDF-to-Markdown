#!/bin/bash
# Setup script for PDF to Markdown MCP Server integration with GitHub Copilot Chat

echo "🚀 Setting up PDF to Markdown MCP Server for GitHub Copilot Chat..."

# Check if we're in the right directory
if [ ! -f "pdf_to_markdown/mcp_server.py" ]; then
    echo "❌ Error: Please run this script from the workspace root directory"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "pdf_to_markdown/venv" ]; then
    echo "📦 Activating virtual environment..."
    source pdf_to_markdown/venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Warning: Virtual environment not found. Installing dependencies globally..."
fi

# Check Python dependencies
echo "🔍 Checking dependencies..."
python -c "import mcp, fitz, PIL" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ All dependencies are installed"
else
    echo "❌ Missing dependencies. Installing..."
    pip install -r pdf_to_markdown/requirements.txt
fi

# Test MCP server
echo "🧪 Testing MCP server..."
python -c "
import sys
sys.path.append('pdf_to_markdown')
try:
    import mcp_server
    print('✅ MCP server imports successfully')
except Exception as e:
    print(f'❌ MCP server error: {e}')
"

# Create VS Code settings directory if it doesn't exist
mkdir -p .vscode

# Create or update VS Code settings for MCP integration
echo "⚙️  Configuring VS Code settings for MCP integration..."

cat > .vscode/settings.json << 'EOF'
{
  "github.copilot.chat.mcp.servers": {
    "pdf-to-markdown": {
      "command": "python",
      "args": ["pdf_to_markdown/mcp_server.py"],
      "cwd": "PDF_WORKSPACE_PATH",
      "env": {},
      "description": "PDF to Markdown Converter with GitHub Copilot Integration",
      "capabilities": ["tools"]
    }
  },
  "github.copilot.chat.mcp.enabled": true
}
EOF

# Replace placeholder with actual workspace path
WORKSPACE_PATH=$(pwd)
sed -i.bak "s|PDF_WORKSPACE_PATH|$WORKSPACE_PATH|g" .vscode/settings.json
rm .vscode/settings.json.bak

echo "✅ VS Code settings configured"

# Test PDF conversion functionality
echo "🧪 Testing PDF conversion functionality..."
python -c "
import sys
sys.path.append('pdf_to_markdown')
try:
    from pdf_to_markdown import PDFToMarkdownConverter
    print('✅ PDF converter imports successfully')
    
    # Test with sample outline PDF if it exists
    import os
    outline_pdf = 'JavaScript-DOM-challenges-TODO-application/v3/Outline.pdf'
    if os.path.exists(outline_pdf):
        print(f'📄 Found sample PDF: {outline_pdf}')
        converter = PDFToMarkdownConverter(outline_pdf, mcp_interactive=False)
        converter.open_pdf()
        print(f'📊 Sample PDF has {len(converter.doc)} pages')
        converter.close_pdf()
        print('✅ PDF processing test successful')
    else:
        print('⚠️  No sample PDF found for testing')
        
except Exception as e:
    print(f'❌ PDF converter error: {e}')
"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Restart VS Code to load the new MCP server configuration"
echo "2. Open GitHub Copilot Chat (Cmd+Shift+I or View > Command Palette > 'Copilot Chat: Open Chat')"
echo "3. The PDF to Markdown tools should now be available in Chat"
echo ""
echo "🔧 Available commands in GitHub Copilot Chat:"
echo "  @pdf-to-markdown Convert this PDF to markdown: path/to/document.pdf"
echo "  @pdf-to-markdown Analyze the structure of path/to/document.pdf"
echo "  @pdf-to-markdown Convert JavaScript-DOM-challenges-TODO-application/v3/Outline.pdf"
echo ""
echo "💬 Example chat prompts:"
echo "  'Convert the Outline.pdf to markdown with enhanced analysis'"
echo "  'Analyze the structure of the JavaScript curriculum PDF'"
echo "  'Extract content from Outline.pdf and preserve formatting'"
echo ""
echo "🔍 To verify the integration:"
echo "  1. Open VS Code Developer Tools (Cmd+Option+I)"
echo "  2. Look for MCP server logs in the Console"
echo "  3. In Copilot Chat, type '@' to see available MCP servers"
echo ""
echo "📁 Workspace structure:"
echo "  - pdf_to_markdown/: Core conversion functionality"
echo "  - .vscode/settings.json: MCP server configuration"
echo "  - Sample PDF: JavaScript-DOM-challenges-TODO-application/v3/Outline.pdf"
echo ""