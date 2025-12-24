# Typhoon OCR - Thai Legal Document Processor

A specialized OCR system for processing Thai legal documents (court verdicts) using Typhoon OCR API and AI-powered text refinement.

## Features

- **OCR Processing**: Extract text from PDF legal documents using Typhoon OCR API
- **AI Refinement**: Post-process extracted text with Gemini AI for legal document formatting
- **Thai Language Support**: Handles Thai numerals, legal terminology, and document structure
- **Batch Processing**: Process multiple PDF files automatically
- **Structured Output**: Organizes legal documents with proper sections and formatting

## Project Structure

```
typhoon-ocr/
├── input/           # Place PDF files here for processing
├── output/          # Raw OCR text output
├── output_revised/  # AI-refined legal documents
├── ocr.py          # Main OCR processing script
├── rewrite.py      # AI text refinement script
├── run_all.sh      # Complete pipeline automation
└── .venv/          # Python virtual environment
```

## Setup

1. **Install Dependencies**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install requests openai pathlib
   ```

2. **Set API Keys**
   ```bash
   export OPENROUTER_API_KEY='your-openrouter-key'
   ```

3. **Add PDF Files**
   Place your Thai legal document PDFs in the `input/` directory.

## Usage

### Complete Pipeline
```bash
./run_all.sh
```

### Individual Steps

**OCR Only:**
```bash
python3 ocr.py
```

**Text Refinement Only:**
```bash
python3 rewrite.py
```

**Process Specific File:**
```bash
python3 rewrite.py --file filename.txt
```

**Limit Processing:**
```bash
python3 rewrite.py --limit 5
```

## Output Format

The system processes Thai Supreme Court verdicts and structures them with:

- **เรื่อง:** Legal references and case citations
- **ประเด็นหลัก:** Main legal issues (from bold text sections)
- **รายละเอียด:** Detailed case information and reasoning

## Configuration

### OCR Settings (ocr.py)
- Model: `typhoon-ocr`
- Pages: 1-22 (configurable)
- Temperature: 0.1
- Max tokens: 16384

### AI Refinement (rewrite.py)
- Model: `google/gemini-3-flash-preview`
- Converts Thai numerals to Arabic
- Removes page numbers and participant names
- Maintains original document structure

## Requirements

- Python 3.7+
- Typhoon OCR API access
- OpenRouter API key for Gemini access
- PDF files containing Thai legal documents

## Notes

- Designed specifically for Thai Supreme Court verdicts
- Preserves legal document integrity while improving readability
- Handles multi-page PDF processing automatically
- Maintains original paragraph structure and legal formatting
