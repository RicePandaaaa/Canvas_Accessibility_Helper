# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Canvas Accessibility Helper - software for updating Canvas LMS courses to be accessible, particularly for use with Simple Syllabus and making accessible figures. The primary functionality is converting VTT (WebVTT video transcript) files into clean, text-only transcripts.

## Architecture

### VTT to Text Conversion Pipeline

The main script (`vtt_to_transcript.py`) is a batch processor that:
1. Scans `transcripts_to_translate/` for all `.vtt` files
2. Skips the VTT header (first 2 lines)
3. Parses VTT chunks (separated by blank lines `\n\n`)
4. Extracts text from each chunk (last element after splitting on `\n`)
5. Removes `<v ->` speaker tags
6. Reconstructs sentences by concatenating text until terminal punctuation (`.`, `!`, `?`)
7. Outputs to `text_only_finished_transcripts/` with `TEXTONLY_` prefix

### Multimedia Lecture Processing Pipeline

The multimedia script (`multimedia_to_word.py`) combines slide decks, video transcripts, and timing data into accessible Word documents:
1. Discovers exactly 3 files in `multimedia_materials/`: one PDF (slides), one VTT (transcript), one TXT (timestamps)
2. Extracts PDF slides as images (150 DPI)
3. Parses VTT with timestamps preserved
4. Parses slide timestamps from TXT file (MM:SS format)
5. Validates alignment (slide count = timestamp count, timestamps within video duration)
6. Segments transcript by timestamp ranges
7. Reconstructs sentences (reuses logic from `vtt_to_transcript.py`)
8. Generates Word document with alternating slide images and transcript segments
9. Outputs to `multimedia_finished_transcripts/` with `MULTIMEDIA_` prefix

**Dependencies:** Requires `poppler` binary for PDF processing:
- **Windows:** Download from https://github.com/oschwartz10612/poppler-windows/releases/, extract and add the `bin` folder to your PATH, OR use `conda install -c conda-forge poppler` (if using conda)
- **macOS:** `brew install poppler`
- **Linux:** `sudo apt-get install poppler-utils`

### Directory Structure

Input/output directories maintain separation and are designed to keep actual content private while preserving folder structure in Git:
- `transcripts_to_translate/` - Place `.vtt` files here for text-only transcript processing
- `text_only_finished_transcripts/` - Script outputs cleaned text files here
- `multimedia_materials/` - Place PDF, VTT, and timestamp files for multimedia processing
- `multimedia_finished_transcripts/` - Multimedia script outputs Word documents here

## Development Setup

**Package Management**: This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install dependencies
uv sync

# Run the main script
uv run vtt_to_transcript.py
```

**Python Version**: Requires Python >=3.13 (specified in `pyproject.toml`)

## Working with Transcripts

### Text-Only Transcripts

To process VTT files into plain text:
1. Place `.vtt` files in `transcripts_to_translate/`
2. Run `uv run vtt_to_transcript.py`
3. Find output in `text_only_finished_transcripts/` with `TEXTONLY_` prefix

The script processes all `.vtt` files in the input directory in a single run - no need to specify individual files.

### Multimedia Transcripts (Slides + Transcript)

To create accessible Word documents combining slides with transcripts:
1. Place exactly 3 files in `multimedia_materials/`:
   - **One PDF file** - Slide deck exported from PowerPoint/Google Slides
   - **One VTT file** - Video transcript from Canvas
   - **One TXT file** - Slide timestamps in MM:SS format (one per line)
2. Create the timestamp file by noting when each slide appears in the video:
   ```
   00:00
   01:30
   03:15
   ```
   Or for longer videos:
   ```
   0:00:00
   0:01:30
   1:05:30
   ```
   (First timestamp must be 00:00 or 0:00:00, number of timestamps must match number of slides)
3. Run `uv run multimedia_to_word.py`
4. Find output in `multimedia_finished_transcripts/` with `MULTIMEDIA_` prefix

**Timestamp File Format:**
- One timestamp per line in HH:MM:SS or MM:SS format (hours optional, defaults to 0)
- Examples: `01:30`, `1:30`, `1:05:30`, `0:01:30`
- First timestamp must be `00:00` or `0:00:00`
- Timestamps must be in ascending order
- Number of timestamps must equal number of slides in the PDF

**Output Format:**
The Word document contains alternating slide images and transcript text:
- Each slide image appears at 6 inches wide
- Transcript text spoken during that slide's time range appears below
- Sections with no transcript show "(No transcript for this section)"

## Notes

- The project has Google Colab support (recent addition)
- Content directories are kept private via `.gitignore` but directory structure is preserved in version control
- VTT format assumption: standard WebVTT structure with header, timestamps, and text chunks separated by blank lines
