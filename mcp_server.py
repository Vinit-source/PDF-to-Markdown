#!/usr/bin/env python3
"""
MCP Server for PDF to Markdown Conversion

This MCP server provides tools for converting PDF files to Markdown format
with LLM-enhanced structure detection and formatting preservation.
"""

import asyncio
import json
import tempfile
import base64
from pathlib import Path
from typing import Any, Sequence
import logging

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.types as types

from pdf_to_markdown import PDFToMarkdownConverter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pdf-to-markdown-mcp")

# Create the server instance
server = Server("pdf-to-markdown")


@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="file://converter-info",
            name="PDF to Markdown Converter Information",
            description="Information about the PDF to Markdown converter capabilities",
            mimeType="text/plain",
        )
    ]


@server.read_resource()
async def handle_read_resource(uri: types.AnyUrl) -> str:
    """Read a specific resource."""
    if uri == "file://converter-info":
        return """PDF to Markdown Converter

This MCP server provides intelligent PDF to Markdown conversion with the following features:

1. **Smart Structure Detection**: Uses LLM analysis to identify document hierarchy
2. **Format Preservation**: Maintains headings, lists, tables, and formatting
3. **Image Extraction**: Extracts and references images from PDFs
4. **Link Preservation**: Maintains internal and external links
5. **Flexible Output**: Customizable output directory and filename

Available Tools:
- convert_pdf_to_markdown: Convert a PDF file to Markdown format
- convert_pdf_from_base64: Convert a base64-encoded PDF to Markdown
- analyze_pdf_structure: Analyze PDF structure without full conversion

Configuration:
- Supports optional LLM API integration for enhanced structure detection
- Falls back to heuristic-based analysis if LLM is not available
- Configurable image extraction and output formatting
"""
    else:
        raise ValueError(f"Unknown resource: {uri}")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="convert_pdf_to_markdown",
            description="Convert a PDF file to Markdown format with smart structure detection",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdf_path": {
                        "type": "string",
                        "description": "Path to the PDF file to convert"
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Output directory for the markdown file and images (optional)"
                    },
                    "output_name": {
                        "type": "string",
                        "description": "Name for the output markdown file (optional)"
                    },
                    "extract_images": {
                        "type": "boolean",
                        "description": "Whether to extract images from the PDF (default: true)",
                        "default": True
                    },
                    "llm_api_url": {
                        "type": "string",
                        "description": "LLM API URL for enhanced structure detection (optional)"
                    },
                    "llm_api_key": {
                        "type": "string",
                        "description": "LLM API key for authentication (optional)"
                    }
                },
                "required": ["pdf_path"]
            }
        ),
        Tool(
            name="convert_pdf_from_base64",
            description="Convert a base64-encoded PDF to Markdown format",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdf_base64": {
                        "type": "string",
                        "description": "Base64-encoded PDF content"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Original filename of the PDF (for naming output)"
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Output directory for the markdown file and images (optional)"
                    },
                    "extract_images": {
                        "type": "boolean",
                        "description": "Whether to extract images from the PDF (default: true)",
                        "default": True
                    },
                    "llm_api_url": {
                        "type": "string",
                        "description": "LLM API URL for enhanced structure detection (optional)"
                    },
                    "llm_api_key": {
                        "type": "string",
                        "description": "LLM API key for authentication (optional)"
                    }
                },
                "required": ["pdf_base64", "filename"]
            }
        ),
        Tool(
            name="analyze_pdf_structure",
            description="Analyze PDF structure and return document hierarchy without full conversion",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdf_path": {
                        "type": "string",
                        "description": "Path to the PDF file to analyze"
                    },
                    "llm_api_url": {
                        "type": "string",
                        "description": "LLM API URL for enhanced structure detection (optional)"
                    },
                    "llm_api_key": {
                        "type": "string",
                        "description": "LLM API key for authentication (optional)"
                    }
                },
                "required": ["pdf_path"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls."""
    if arguments is None:
        arguments = {}
    
    try:
        if name == "convert_pdf_to_markdown":
            return await convert_pdf_to_markdown(arguments)
        elif name == "convert_pdf_from_base64":
            return await convert_pdf_from_base64(arguments)
        elif name == "analyze_pdf_structure":
            return await analyze_pdf_structure(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}")
        return [
            types.TextContent(
                type="text",
                text=f"Error: {str(e)}"
            )
        ]


async def convert_pdf_to_markdown(arguments: dict) -> list[types.TextContent]:
    """Convert a PDF file to Markdown format."""
    pdf_path = arguments["pdf_path"]
    output_dir = arguments.get("output_dir")
    output_name = arguments.get("output_name")
    extract_images = arguments.get("extract_images", True)
    llm_api_url = arguments.get("llm_api_url")
    llm_api_key = arguments.get("llm_api_key")
    
    # Validate PDF file exists
    if not Path(pdf_path).exists():
        raise ValueError(f"PDF file not found: {pdf_path}")
    
    # Create converter
    converter = PDFToMarkdownConverter(
        pdf_path=pdf_path,
        output_dir=output_dir,
        extract_images=extract_images,
        llm_api_url=llm_api_url,
        llm_api_key=llm_api_key
    )
    
    # Convert PDF
    output_path = converter.convert(output_name)
    
    # Read the generated markdown
    with open(output_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    
    # Return results
    results = [
        types.TextContent(
            type="text",
            text=f"Successfully converted PDF to Markdown!\n\nOutput file: {output_path}\n\n--- Generated Markdown ---\n\n{markdown_content}"
        )
    ]
    
    return results


async def convert_pdf_from_base64(arguments: dict) -> list[types.TextContent]:
    """Convert a base64-encoded PDF to Markdown format."""
    pdf_base64 = arguments["pdf_base64"]
    filename = arguments["filename"]
    output_dir = arguments.get("output_dir")
    extract_images = arguments.get("extract_images", True)
    llm_api_url = arguments.get("llm_api_url")
    llm_api_key = arguments.get("llm_api_key")
    
    # Decode base64 PDF
    try:
        pdf_data = base64.b64decode(pdf_base64)
    except Exception as e:
        raise ValueError(f"Invalid base64 data: {e}")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        temp_file.write(pdf_data)
        temp_pdf_path = temp_file.name
    
    try:
        # Set output directory to temp if not specified
        if not output_dir:
            output_dir = Path(temp_pdf_path).parent
        
        # Create converter
        converter = PDFToMarkdownConverter(
            pdf_path=temp_pdf_path,
            output_dir=output_dir,
            extract_images=extract_images,
            llm_api_url=llm_api_url,
            llm_api_key=llm_api_key
        )
        
        # Convert PDF
        output_name = Path(filename).stem + ".md"
        output_path = converter.convert(output_name)
        
        # Read the generated markdown
        with open(output_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()
        
        return [
            types.TextContent(
                type="text",
                text=f"Successfully converted PDF from base64 to Markdown!\n\nOriginal filename: {filename}\nOutput file: {output_path}\n\n--- Generated Markdown ---\n\n{markdown_content}"
            )
        ]
    
    finally:
        # Clean up temporary file
        Path(temp_pdf_path).unlink()


async def analyze_pdf_structure(arguments: dict) -> list[types.TextContent]:
    """Analyze PDF structure without full conversion."""
    pdf_path = arguments["pdf_path"]
    llm_api_url = arguments.get("llm_api_url")
    llm_api_key = arguments.get("llm_api_key")
    
    # Validate PDF file exists
    if not Path(pdf_path).exists():
        raise ValueError(f"PDF file not found: {pdf_path}")
    
    # Create converter for analysis
    converter = PDFToMarkdownConverter(
        pdf_path=pdf_path,
        extract_images=False,
        llm_api_url=llm_api_url,
        llm_api_key=llm_api_key
    )
    
    try:
        converter.open_pdf()
        
        analysis_results = {
            "document_info": {
                "path": pdf_path,
                "pages": len(converter.doc),
                "metadata": converter.doc.metadata
            },
            "structure_analysis": []
        }
        
        # Analyze first few pages for structure
        max_pages = min(3, len(converter.doc))
        
        for page_num in range(max_pages):
            page = converter.doc[page_num]
            
            # Extract text with formatting
            text_blocks = converter.extract_text_with_formatting(page)
            
            # Analyze structure
            structure = converter.analyze_structure_with_llm(text_blocks)
            
            analysis_results["structure_analysis"].append({
                "page": page_num + 1,
                "structure": structure,
                "block_count": len([b for b in text_blocks if b["type"] == "text"])
            })
        
        return [
            types.TextContent(
                type="text",
                text=f"PDF Structure Analysis Results:\n\n{json.dumps(analysis_results, indent=2)}"
            )
        ]
    
    finally:
        converter.close_pdf()


async def main():
    """Main function to run the MCP server."""
    # Import here to avoid issues with event loop
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="pdf-to-markdown",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())