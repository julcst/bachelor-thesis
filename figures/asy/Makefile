# A Makefile for Asymptote that runs every .asy file in the current directory and outputs a PDF for each.
# Usage: make
# This Makefile assumes that Asymptote is installed and available in the PATH.
# It also assumes that the output files will be named after the input files with a .pdf extension.
# To clean up the generated files, use: make clean
.PHONY: all clean
all: $(patsubst %.asy, %.pdf, $(wildcard *.asy))
%.pdf: %.asy
	asy -f pdf $<
clean:
	rm -f *.pdf *.log *.aux *.eps *.png *.svg