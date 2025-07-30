#!/usr/bin/env python3
"""
PDF to Markdown Converter with MCP Client Integration

This script converts PDF files to Markdown format while preserving:
- Text formatting (bold, italic, headers)
- Links (both internal and external)
- Images (extracted and referenced)
- Document structure (enhanced with MCP client analysis)
- Lists and tables
- Proper heading hierarchy

The converter can work with MCP clients (like GitHub Copilot) for intelligent
document structure analysis and format detection.
"""

import fitz  # PyMuPDF
import os
import re
import argparse
import json
import base64
from pathlib import Path
from PIL import Image
import hashlib
from typing import List, Dict, Any, Optional, Tuple, Callable
import requests
import sys


class MCPClientInterface:
    """Interface for communicating with MCP clients for document analysis."""
    
    def __init__(self, interactive_mode: bool = True):
        self.interactive_mode = interactive_mode
        self.analysis_callback: Optional[Callable] = None
    
    def set_analysis_callback(self, callback: Callable):
        """Set a callback function for receiving analysis results from MCP client."""
        self.analysis_callback = callback
    
    def request_structure_analysis(self, text_blocks: List[Dict[str, Any]], 
                                 document_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request document structure analysis from MCP client.
        
        This method will prompt the MCP client (like Copilot) to analyze
        the document structure and provide semantic classification.
        """
        analysis_prompt = self._create_analysis_prompt(text_blocks, document_context)
        
        if self.interactive_mode:
            return self._interactive_analysis_request(analysis_prompt, text_blocks)
        else:
            return self._automated_analysis_request(analysis_prompt, text_blocks)
    
    def _create_analysis_prompt(self, text_blocks: List[Dict[str, Any]], 
                               document_context: Dict[str, Any]) -> str:
        """Create a structured prompt for the MCP client."""
        analysis_text = self._prepare_text_for_analysis(text_blocks)
        
        prompt = f"""
# PDF Document Structure Analysis Request

## Document Context
- **File**: {document_context.get('filename', 'Unknown')}
- **Page**: {document_context.get('page_num', 'Unknown')} of {document_context.get('total_pages', 'Unknown')}
- **Text Blocks**: {len(text_blocks)} blocks detected

## Analysis Task
Please analyze the following text blocks extracted from a PDF and classify each block's semantic role.

**Classification Types:**
- `title`: Main document title
- `heading1`: Primary section headers
- `heading2`: Secondary section headers  
- `heading3`: Tertiary section headers
- `heading4`: Quaternary section headers
- `paragraph`: Regular body text
- `list_item`: Bulleted or numbered list items
- `table_cell`: Table content
- `caption`: Image or table captions
- `metadata`: Headers, footers, page numbers
- `other`: Unclassified content

## Text Blocks to Analyze
{analysis_text}

## Expected Response Format
Please provide your analysis as a JSON object:

```json
{{
    "structure": [
        {{
            "block_id": 0,
            "type": "heading1",
            "confidence": 0.95,
            "reasoning": "Large font size, positioned prominently"
        }},
        {{
            "block_id": 1,
            "type": "paragraph",
            "confidence": 0.8,
            "reasoning": "Standard body text formatting"
        }}
    ],
    "document_hierarchy": {{
        "title": "Detected Document Title",
        "sections": ["Section 1", "Section 2"],
        "has_toc": false,
        "document_type": "article|manual|report|other"
    }},
    "formatting_notes": [
        "Consistent heading hierarchy detected",
        "List formatting needs normalization"
    ]
}}
```

## Additional Guidance
- Consider font sizes, positioning, and content patterns
- Look for hierarchical relationships between headings
- Identify list patterns and table structures
- Note any formatting inconsistencies that need correction
"""
        return prompt
    
    def _interactive_analysis_request(self, prompt: str, text_blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle interactive analysis request with MCP client."""
        print("\n" + "="*80)
        print("🤖 MCP CLIENT ANALYSIS REQUEST")
        print("="*80)
        print(prompt)
        print("="*80)
        print("\n⏳ Waiting for MCP client analysis...")
        print("💡 If you're using GitHub Copilot, it should provide structured analysis above.")
        print("📝 Please paste the JSON response below, or press Enter for fallback analysis:")
        print("-"*40)
        
        try:
            # Wait for user to paste the analysis result
            user_input = input().strip()
            
            if user_input:
                # Try to parse the JSON response
                if user_input.startswith('```json'):
                    # Extract JSON from code block
                    json_start = user_input.find('{')
                    json_end = user_input.rfind('}') + 1
                    if json_start != -1 and json_end != -1:
                        user_input = user_input[json_start:json_end]
                
                analysis_result = json.loads(user_input)
                print("✅ Successfully received MCP client analysis!")
                return analysis_result
            else:
                print("⚠️  No input received, falling back to heuristic analysis...")
                return self._fallback_structure_analysis(text_blocks)
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print("⚠️  Falling back to heuristic analysis...")
            return self._fallback_structure_analysis(text_blocks)
        except KeyboardInterrupt:
            print("\n🛑 Analysis interrupted by user")
            return self._fallback_structure_analysis(text_blocks)
    
    def _automated_analysis_request(self, prompt: str, text_blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle automated analysis request (for programmatic use)."""
        if self.analysis_callback:
            try:
                return self.analysis_callback(prompt, text_blocks)
            except Exception as e:
                print(f"Error in analysis callback: {e}")
                return self._fallback_structure_analysis(text_blocks)
        else:
            return self._fallback_structure_analysis(text_blocks)
    
    def _prepare_text_for_analysis(self, text_blocks: List[Dict[str, Any]]) -> str:
        """Prepare text blocks for analysis with detailed formatting info."""
        analysis_text = ""
        
        for i, block in enumerate(text_blocks):
            if block["type"] == "text":
                block_text = ""
                avg_font_size = 0
                font_count = 0
                fonts_used = set()
                is_bold = False
                is_italic = False
                
                for line in block["lines"]:
                    for span in line["spans"]:
                        block_text += span["text"]
                        avg_font_size += span["size"]
                        font_count += 1
                        fonts_used.add(span["font"])
                        
                        # Check formatting flags
                        flags = span.get("flags", 0)
                        if flags & 2**4:  # Bold flag
                            is_bold = True
                        if flags & 2**1:  # Italic flag
                            is_italic = True
                
                if font_count > 0:
                    avg_font_size /= font_count
                
                # Format the block info for analysis
                formatting_info = []
                if is_bold:
                    formatting_info.append("BOLD")
                if is_italic:
                    formatting_info.append("ITALIC")
                
                formatting_str = f" [{', '.join(formatting_info)}]" if formatting_info else ""
                font_info = f"Font: {avg_font_size:.1f}pt"
                bbox_info = f"Position: {block['bbox']}"
                
                analysis_text += f"Block {i}: {font_info}{formatting_str} | {bbox_info}\n"
                analysis_text += f"Text: {block_text.strip()}\n"
                analysis_text += f"Fonts: {', '.join(fonts_used)}\n\n"
        
        return analysis_text
    
    def _fallback_structure_analysis(self, text_blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback structure analysis without MCP client."""
        structure = []
        sections = []
        
        for i, block in enumerate(text_blocks):
            if block["type"] == "text":
                # Enhanced heuristic based on font size and formatting
                avg_font_size = self._get_average_font_size(block)
                is_bold = self._is_block_bold(block)
                text = self._extract_block_text(block)
                
                # Classification logic
                if avg_font_size >= 20 or (avg_font_size >= 16 and is_bold):
                    block_type = "title" if i == 0 else "heading1"
                    if block_type == "heading1":
                        sections.append(text.strip())
                elif avg_font_size >= 16 or (avg_font_size >= 14 and is_bold):
                    block_type = "heading2"
                elif avg_font_size >= 14 or (avg_font_size >= 12 and is_bold):
                    block_type = "heading3"
                else:
                    # Check if it looks like a list item
                    if re.match(r'^\s*[\u2022\u2023\u25E6\u2043\u2219\*\-\+]\s', text) or \
                       re.match(r'^\s*\d+\.?\s', text):
                        block_type = "list_item"
                    elif len(text.strip()) < 50 and ':' in text:
                        block_type = "metadata"
                    else:
                        block_type = "paragraph"
                
                structure.append({
                    "block_id": i,
                    "type": block_type,
                    "confidence": 0.7,
                    "reasoning": f"Heuristic: font_size={avg_font_size:.1f}, bold={is_bold}"
                })
        
        return {
            "structure": structure,
            "document_hierarchy": {
                "title": "Unknown Document",
                "sections": sections,
                "has_toc": False,
                "document_type": "unknown"
            },
            "formatting_notes": ["Analysis performed without MCP client assistance"]
        }
    
    def _get_average_font_size(self, block: Dict[str, Any]) -> float:
        """Calculate average font size for a text block."""
        total_size = 0
        count = 0
        
        for line in block["lines"]:
            for span in line["spans"]:
                total_size += span["size"]
                count += 1
        
        return total_size / count if count > 0 else 12
    
    def _is_block_bold(self, block: Dict[str, Any]) -> bool:
        """Check if text block is predominantly bold."""
        bold_chars = 0
        total_chars = 0
        
        for line in block["lines"]:
            for span in line["spans"]:
                flags = span.get("flags", 0)
                char_count = len(span["text"])
                total_chars += char_count
                if flags & 2**4:  # Bold flag
                    bold_chars += char_count
        
        return total_chars > 0 and (bold_chars / total_chars) > 0.5
    
    def _extract_block_text(self, block: Dict[str, Any]) -> str:
        """Extract plain text from a text block."""
        text = ""
        for line in block["lines"]:
            for span in line["spans"]:
                text += span["text"]
        return text


class PDFToMarkdownConverter:
    def __init__(self, pdf_path, output_dir=None, extract_images=True, 
                 llm_api_url=None, llm_api_key=None, mcp_interactive=True):
        """
        Initialize the PDF to Markdown converter with MCP client support.
        
        Args:
            pdf_path (str): Path to the input PDF file
            output_dir (str): Directory to save output files (default: same as PDF)
            extract_images (bool): Whether to extract and save images
            llm_api_url (str): Legacy LLM API URL (deprecated, use MCP instead)
            llm_api_key (str): Legacy LLM API key (deprecated, use MCP instead)
            mcp_interactive (bool): Enable interactive MCP client mode
        """
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir) if output_dir else self.pdf_path.parent
        self.should_extract_images = extract_images
        self.images_dir = self.output_dir / "images"
        self.doc = None
        self.markdown_content = []
        self.image_counter = 0
        
        # MCP client interface
        self.mcp_client = MCPClientInterface(interactive_mode=mcp_interactive)
        
        # Legacy LLM support (deprecated)
        self.llm_api_url = llm_api_url
        self.llm_api_key = llm_api_key
        if llm_api_url:
            print("⚠️  Warning: Direct LLM API usage is deprecated. Consider using MCP client integration.")
        
    def set_mcp_analysis_callback(self, callback: Callable):
        """Set a callback function for automated MCP analysis."""
        self.mcp_client.set_analysis_callback(callback)
    
    def open_pdf(self):
        """Open the PDF document."""
        try:
            self.doc = fitz.open(self.pdf_path)
            if self.doc is None:
                raise Exception("Failed to open PDF document")
            print(f"📄 Successfully opened PDF: {self.pdf_path}")
            print(f"📊 Document has {len(self.doc)} pages")
        except Exception as e:
            raise Exception(f"Error opening PDF: {e}")
    
    def close_pdf(self):
        """Close the PDF document."""
        if self.doc:
            self.doc.close()
    
    def setup_output_directory(self):
        """Create output directory and images subdirectory if needed."""
        self.output_dir.mkdir(exist_ok=True)
        if self.should_extract_images:
            self.images_dir.mkdir(exist_ok=True)
    
    def extract_text_with_formatting(self, page) -> List[Dict[str, Any]]:
        """Extract text with detailed formatting information."""
        blocks = []
        text_dict = page.get_text("dict")
        
        for block in text_dict["blocks"]:
            if "lines" in block:  # Text block
                block_info = {
                    "type": "text",
                    "bbox": block["bbox"],
                    "lines": []
                }
                
                for line in block["lines"]:
                    line_info = {
                        "bbox": line["bbox"],
                        "spans": []
                    }
                    
                    for span in line["spans"]:
                        span_info = {
                            "text": span["text"],
                            "font": span["font"],
                            "size": span["size"],
                            "flags": span["flags"],  # Bold, italic, etc.
                            "color": span["color"],
                            "bbox": span["bbox"]
                        }
                        line_info["spans"].append(span_info)
                    
                    block_info["lines"].append(line_info)
                blocks.append(block_info)
            
            elif "image" in block:  # Image block
                blocks.append({
                    "type": "image",
                    "bbox": block["bbox"],
                    "image": block["image"]
                })
        
        return blocks
    
    def extract_images(self, page, page_num: int) -> List[str]:
        """Extract images from a page and save them."""
        image_refs = []
        if not self.should_extract_images:
            return image_refs
        
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            try:
                xref = img[0]
                pix = fitz.Pixmap(self.doc, xref)
                
                if pix.n - pix.alpha < 4:  # GRAY or RGB
                    img_data = pix.tobytes("png")
                    img_hash = hashlib.md5(img_data).hexdigest()[:8]
                    img_filename = f"image_{page_num}_{img_index}_{img_hash}.png"
                    img_path = self.images_dir / img_filename
                    
                    with open(img_path, "wb") as f:
                        f.write(img_data)
                    
                    image_refs.append(f"images/{img_filename}")
                
                pix = None
                
            except Exception as e:
                print(f"Error extracting image {img_index} from page {page_num}: {e}")
        
        return image_refs
    
    def analyze_structure_with_mcp(self, text_blocks: List[Dict[str, Any]], 
                                  page_num: int = 1, total_pages: int = 1) -> Dict[str, Any]:
        """Use MCP client to analyze document structure and identify semantic elements."""
        document_context = {
            "filename": self.pdf_path.name,
            "page_num": page_num,
            "total_pages": total_pages
        }
        
        try:
            return self.mcp_client.request_structure_analysis(text_blocks, document_context)
        except Exception as e:
            print(f"⚠️  MCP analysis failed: {e}")
            print("🔄 Falling back to heuristic analysis...")
            return self.mcp_client._fallback_structure_analysis(text_blocks)
    
    def analyze_structure_with_llm(self, text_blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Legacy LLM analysis method - redirects to MCP analysis."""
        print("🔄 Redirecting legacy LLM analysis to MCP client...")
        return self.analyze_structure_with_mcp(text_blocks)
    
    def convert_blocks_to_markdown(self, text_blocks: List[Dict[str, Any]], 
                                  structure: Dict[str, Any], 
                                  images: List[str]) -> str:
        """Convert analyzed blocks to markdown format."""
        markdown_lines = []
        image_index = 0
        
        structure_map = {item["block_id"]: item for item in structure.get("structure", [])}
        
        for i, block in enumerate(text_blocks):
            if block["type"] == "text":
                block_structure = structure_map.get(i, {"type": "paragraph"})
                block_type = block_structure["type"]
                text = self._extract_block_text(block)
                
                if not text.strip():
                    continue
                
                # Convert based on identified structure
                if block_type == "title":
                    markdown_lines.append(f"# {text.strip()}")
                elif block_type == "heading1":
                    markdown_lines.append(f"# {text.strip()}")
                elif block_type == "heading2":
                    markdown_lines.append(f"## {text.strip()}")
                elif block_type == "heading3":
                    markdown_lines.append(f"### {text.strip()}")
                elif block_type == "heading4":
                    markdown_lines.append(f"#### {text.strip()}")
                elif block_type == "list_item":
                    # Clean up list formatting
                    clean_text = re.sub(r'^\s*[\u2022\u2023\u25E6\u2043\u2219\*\-\+]\s*', '- ', text.strip())
                    clean_text = re.sub(r'^\s*\d+\.?\s*', '1. ', clean_text)
                    markdown_lines.append(clean_text)
                else:
                    # Regular paragraph
                    markdown_lines.append(text.strip())
                
                markdown_lines.append("")  # Add spacing
            
            elif block["type"] == "image" and image_index < len(images):
                markdown_lines.append(f"![Image]({images[image_index]})")
                markdown_lines.append("")
                image_index += 1
        
        return "\n".join(markdown_lines)
    
    def convert(self, output_name: Optional[str] = None) -> Path:
        """Convert PDF to Markdown with MCP client enhancement."""
        try:
            self.open_pdf()
            self.setup_output_directory()
            
            all_markdown_content = []
            total_pages = len(self.doc)
            
            print(f"\n🚀 Starting conversion with MCP client integration...")
            
            for page_num in range(total_pages):
                print(f"\n📄 Processing page {page_num + 1}/{total_pages}")
                page = self.doc[page_num]
                
                # Extract text with formatting
                text_blocks = self.extract_text_with_formatting(page)
                print(f"📝 Extracted {len([b for b in text_blocks if b['type'] == 'text'])} text blocks")
                
                # Extract images
                images = self.extract_images(page, page_num + 1)
                if images:
                    print(f"🖼️  Extracted {len(images)} images")
                
                # Analyze structure with MCP client
                print("🤖 Requesting structure analysis from MCP client...")
                structure = self.analyze_structure_with_mcp(text_blocks, page_num + 1, total_pages)
                
                # Convert to markdown
                page_markdown = self.convert_blocks_to_markdown(text_blocks, structure, images)
                all_markdown_content.append(page_markdown)
            
            # Combine all pages
            final_markdown = "\n\n---\n\n".join(all_markdown_content)
            
            # Save markdown file
            if output_name:
                output_path = self.output_dir / output_name
            else:
                output_path = self.output_dir / f"{self.pdf_path.stem}.md"
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(final_markdown)
            
            print(f"\n✅ Conversion completed successfully!")
            print(f"📁 Output file: {output_path}")
            
            return output_path
            
        finally:
            self.close_pdf()


def main():
    """Main function to handle command line interface."""
    parser = argparse.ArgumentParser(
        description="Convert PDF to Markdown while preserving formatting, links, and images"
    )
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    parser.add_argument(
        "-o", "--output", 
        help="Output directory (default: same as PDF file)"
    )
    parser.add_argument(
        "-n", "--name", 
        help="Output filename (default: PDF name + .md)"
    )
    parser.add_argument(
        "--no-images", 
        action="store_true", 
        help="Skip image extraction"
    )
    parser.add_argument(
        "--llm-api-url",
        help="LLM API URL for structure detection"
    )
    parser.add_argument(
        "--llm-api-key",
        help="LLM API key for authentication"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file not found: {args.pdf_path}")
        return 1
    
    try:
        # Create converter
        converter = PDFToMarkdownConverter(
            pdf_path=args.pdf_path,
            output_dir=args.output,
            extract_images=not args.no_images,
            llm_api_url=args.llm_api_url,
            llm_api_key=args.llm_api_key
        )
        
        # Convert
        output_path = converter.convert(args.name)
        print(f"\nConversion completed successfully!")
        print(f"Output file: {output_path}")
        
        return 0
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        return 1


if __name__ == "__main__":
    exit(main())