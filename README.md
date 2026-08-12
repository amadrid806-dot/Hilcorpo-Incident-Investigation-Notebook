# Hilcorp Incident Investigation Field Notebook

A programmatically generated, reMarkable-optimized incident investigation field notebook for upstream oil & gas operations.

## What this project builds

The generator produces four polished 24-page releases plus a combined **96-page Version 1.0 notebook**:

1. **Release 01 - Foundation**: cover, contents, use guide, incident information, notifications, immediate response, notes.
2. **Release 02 - Investigation**: interviews, timeline, scene documentation, evidence and photo logs.
3. **Release 03 - Analysis**: equipment/energy, human factors, barrier/root-cause analysis, corrective actions.
4. **Release 04 - Reference**: lessons learned, field quick references, sketch library, notes.

The combined PDF includes PDF bookmarks and clickable top navigation tabs when the target section exists in the document.

## Local build

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

python -m pip install -r requirements.txt
python source/build_notebook.py
```

Build Letter, A4 and reMarkable variants:

```bash
python source/build_notebook.py --all-formats
```

Outputs are written to `output/`.

## GitHub Actions

The included workflow builds the PDFs whenever the notebook source changes and uploads them as a workflow artifact.

## Branding

`assets/logo/hilcorp_logo.jpg` is the logo supplied by the project owner for this project. Do not replace it with an internet-sourced logo.

## Design principles

- Handwriting first.
- High contrast for e-ink.
- Minimal visual clutter.
- Large stylus-friendly targets and checkboxes.
- General oil & gas terminology; no incident-specific content.
- Open-ended, evidence-based, learning-focused prompts.
- Consistent cross-section navigation.

## Project roadmap

Future companion deliverables can reuse the same design system:

- Investigation report PowerPoint template
- Corrective action tracker (Excel)
- Lessons learned bulletin
- Investigation checklist cards
