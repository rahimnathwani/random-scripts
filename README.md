# CLI Utilities

A collection of useful command-line utilities for document processing and manipulation.

## Tools

### 1. markdown-link-transformer.py

Transforms markdown files by replacing link text with just the domain name.

**Usage Example:**
```bash
cat myarticle.md | ./markdown-link-transformer.py > transformed.md
```

This will convert markdown links like:
- `[Check out this awesome article](https://example.com/article)` 
- to: `[example.com](https://example.com/article)`

Useful for cleaning up articles with too many descriptive link texts when you want to make it clear where links lead to.

It's particularly useful for reports that have come out of OpenAI's Deep Research. At the time of writing (2025-03-12), the UI displays only the domain name of each link, but when you copy the content to paste into a doc or whatever, the link text is the full title from doc. If you don't want this, just pipe the output through this script before pasting into your target, e.g.

```bash
pbpaste | ./markdown-link-transformer.py | pbcopy
```

### 2. pdf-search.py

Extracts text from PDF files with encoding information. Shows both the encoded representation of text (with font size information) and the rendered text.

**Usage Example:**
```bash
./pdf-search.py document.pdf
```

Output will display lines like:
```
(H)12(e)12(l)12(l)12(o)12 | Hello
```

This tool is particularly useful for diagnosing PDF text extraction issues or understanding how text is encoded in PDFs.

### 3. process-pdf.sh

Processes a PDF file by extracting only grayscale images, negating them, and creating a new black-and-white PDF. It's most useful for MRC PDFs, e.g. made with Internet Archive's archive-pdf-tools package.

**Usage Example:**
```bash
./process-pdf.sh original.pdf
```

This will create a new file called `original-bw.pdf` in the same directory as the input file, containing only grayscale images from the original PDF with inverted colors.

### 4. transcribe-mp3.sh

Transcribes MP3 audio files to text using Whisper speech recognition.

**Usage Example:**
```bash
./transcribe-mp3.sh recording.mp3
```

This will create a text file `recording.txt` containing the transcription of the audio content.

Note: Requires `ffmpeg` and `whisper-cli` to be installed on your system. The script uses a specific whisper model at `/Users/rahim/src/public/whisper.cpp/models/ggml-large-v3-turbo.bin`.

## Installation

No specific installation required beyond ensuring that all dependencies are installed. Most scripts use [uv](https://github.com/astral-sh/uv) for Python dependency management through script headers.

Dependencies:
- Python 3.8+ (for Python scripts)
- uv (for Python dependency management)
- ImageMagick (`convert` and `identify` commands)
- mutool (from MuPDF)
- ffmpeg
- whisper-cli (with appropriate models)

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

