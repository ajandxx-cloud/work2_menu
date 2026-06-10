# Manuscript

This directory contains the English LaTeX draft for the work2 paper.

## Build Workflow

Refresh tables and figures, then compile when a LaTeX compiler is installed:

```powershell
python scripts/build_manuscript.py
```

If the machine does not have `latexmk` or `pdflatex`, you can still refresh the linked artifacts and manuscript metadata:

```powershell
python scripts/build_manuscript.py --skip_compile
```

## Structure

- `main.tex`: paper entrypoint
- `sections/`: section files
- `references.bib`: bibliography placeholder file
- `build/`: generated build metadata and compiled PDF when available
