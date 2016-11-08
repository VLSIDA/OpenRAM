#!/bin/sh
# This is a short script to simplify generating a PDF document from LaTeX and BibTeX code.
# The script cleans plausibly existing files, generates the PDF, then cleans furthur generated files.

# Clean any latent files.
rm -rf *.aux *.bbl *.blg *.log #*.pdf

# Generate the actual output.
pdflatex main.tex 
bibtex main.aux
pdflatex main.tex
pdflatex main.tex
mv main.pdf openram.pdf

# Clean all the generated files except for the .pdf
rm -rf *.aux *.bbl *.blg *.log *.lof *.lot *.out *.toc
