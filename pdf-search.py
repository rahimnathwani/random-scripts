#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pdfminer.six>=20221105",
# ]
# ///

import sys
from typing import Iterator, Tuple
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTChar
from pdfminer.converter import PDFPageAggregator

def extract_text_with_encoding(pdf_path: str) -> Iterator[Tuple[str, str]]:
    """
    Extract text from PDF, yielding tuples of (encoded_text, rendered_text)
    """
    with open(pdf_path, 'rb') as file:
        # Set up PDF parsing
        parser = PDFParser(file)
        document = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # Iterate through pages
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            
            for element in layout:
                if isinstance(element, (LTTextBox, LTTextLine)):
                    # Get the rendered text
                    rendered_text = element.get_text().strip()
                    if not rendered_text:
                        continue
                        
                    # Get the encoded form by examining each character
                    encoded_parts = []
                    for text_line in element:
                        if isinstance(text_line, LTTextLine):
                            for char in text_line:
                                if isinstance(char, LTChar):
                                    # Get font name and size
                                    font_size = round(char.size)
                                    text = char.get_text()
                                    
                                    # Build encoding representation
                                    if text.strip():
                                        encoded_parts.append(f"({text}){font_size}")
                    
                    encoded_text = "".join(encoded_parts)
                    if encoded_text:
                        yield (encoded_text, rendered_text)

def main():
    if len(sys.argv) != 2:
        print("Usage: pdf-text-dump.py <pdf_file>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    
    try:
        print("ENCODED TEXT | RENDERED TEXT")
        print("-" * 60)
        
        for encoded, rendered in extract_text_with_encoding(pdf_file):
            print(f"{encoded} | {rendered}")
            
    except FileNotFoundError:
        print(f"Error: File '{pdf_file}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error processing PDF: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
