#!/usr/bin/env python3
"""
Example usage of the PDF to Markdown Converter

This script demonstrates how to use both the standalone converter
and the MCP server functionality.
"""

import asyncio
import json
import os
from pathlib import Path
from pdf_to_markdown import PDFToMarkdownConverter


async def example_standalone_conversion():
    """Example of using the converter directly."""
    print("=== Standalone PDF to Markdown Conversion ===")
    
    # Example PDF path (you'll need to provide a real PDF)
    pdf_path = "example.pdf"
    
    if not Path(pdf_path).exists():
        print(f"Please place a PDF file at {pdf_path} to run this example")
        return
    
    # Create converter with LLM enhancement (optional)
    converter = PDFToMarkdownConverter(
        pdf_path=pdf_path,
        output_dir="output",
        extract_images=True,
        # Uncomment and configure for LLM enhancement:
        # llm_api_url="https://api.openai.com/v1/chat/completions",
        # llm_api_key="your-api-key-here"
    )
    
    try:
        # Convert PDF to Markdown
        output_path = converter.convert()
        print(f"✅ Conversion completed! Output: {output_path}")
        
        # Read and display first 500 characters
        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()
            print(f"\nFirst 500 characters of output:\n{content[:500]}...")
            
    except Exception as e:
        print(f"❌ Error during conversion: {e}")


async def example_mcp_server_usage():
    """Example of how the MCP server would be used."""
    print("\n=== MCP Server Usage Example ===")
    
    # This demonstrates the tool calls that would be made to the MCP server
    example_tools = [
        {
            "name": "convert_pdf_to_markdown",
            "arguments": {
                "pdf_path": "/path/to/document.pdf",
                "output_dir": "/path/to/output",
                "extract_images": True,
                "llm_api_url": "https://api.openai.com/v1/chat/completions",
                "llm_api_key": "your-api-key"
            }
        },
        {
            "name": "analyze_pdf_structure",
            "arguments": {
                "pdf_path": "/path/to/document.pdf",
                "llm_api_url": "https://api.openai.com/v1/chat/completions",
                "llm_api_key": "your-api-key"
            }
        }
    ]
    
    print("Available MCP tools:")
    for tool in example_tools:
        print(f"- {tool['name']}")
        print(f"  Arguments: {json.dumps(tool['arguments'], indent=4)}")
        print()


def example_smart_structure_detection():
    """Example of the smart algorithm features."""
    print("=== Smart Structure Detection Features ===")
    
    features = {
        "LLM-Enhanced Analysis": [
            "Identifies document hierarchy beyond simple font size rules",
            "Recognizes semantic meaning of text blocks",
            "Detects complex list structures and nested formatting",
            "Understands context for better heading classification"
        ],
        "Fallback Heuristics": [
            "Font size-based heading detection",
            "Pattern matching for list items",
            "Position-based structure analysis",
            "Robust handling when LLM is unavailable"
        ],
        "Format Preservation": [
            "Maintains markdown heading hierarchy (# ## ### ####)",
            "Preserves bullet points and numbered lists",
            "Extracts and references images with proper markdown syntax",
            "Handles complex document layouts"
        ],
        "Smart Processing": [
            "Analyzes font metadata (size, style, positioning)",
            "Groups related text blocks intelligently",
            "Maintains document flow and readability",
            "Handles edge cases and malformed PDFs"
        ]
    }
    
    for category, items in features.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  ✓ {item}")


async def main():
    """Run all examples."""
    print("PDF to Markdown Converter - Example Usage\n")
    
    # Show smart features
    example_smart_structure_detection()
    
    # Show MCP server usage
    await example_mcp_server_usage()
    
    # Try standalone conversion if PDF exists
    await example_standalone_conversion()
    
    print("\n=== Getting Started ===")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run standalone: python pdf_to_markdown.py your_file.pdf")
    print("3. Run MCP server: python mcp_server.py")
    print("4. For LLM enhancement, configure API URL and key")


if __name__ == "__main__":
    asyncio.run(main())