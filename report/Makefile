all: Makefile *.tex *.bib *.cls
	pdflatex paper
	bibtex paper -min-crossrefs=5
	pdflatex paper
	pdflatex paper

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.rel paper.pdf

.PHONY: all clean
