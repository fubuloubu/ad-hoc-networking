# LaTeX makefile for documentation
# Note: run it twice to ensure LastPage works
# For Bibtex, run it 3 times for references
PDFLATEX=pdflatex -shell-escape -interaction=batchmode
BIBTEX=bibtex
IGNORE_OUTPUT=/dev/null
define GET_ERROR
	(echo && echo "Error:" && echo && cat $*.$(1) | grep -A 10 ^! && rm $@ && exit 1)
endef
define RUN_PDFLATEX
	echo " LATEX $<"; \
	$(PDFLATEX) $< > $(IGNORE_OUTPUT) || $(call GET_ERROR,log);
endef
define RUN_BIBTEX
	echo "BIBTEX $<"; \
	$(BIBTEX) $* > $(IGNORE_OUTPUT) || $(call GET_ERROR,blg);
endef
%.pdf: %.tex
	@$(call RUN_PDFLATEX)
	@if [ `grep "bibliography\.bib" $<` ]; then \
		( \
			$(call RUN_BIBTEX) \
			$(call RUN_PDFLATEX) \
		); \
	fi
	@$(call RUN_PDFLATEX)
	@if [ -d "$$(readlink -f ~/Downloads)" ]; then \
		echo "  MOVE $@"; \
		mv $@ ~/Downloads; \
	fi;

# This is to remove extra instructions from matplotlib2tikz
tail_copy=tail -n +$(2) $(1) > $(shell basename $(1));

.PHONY: copy_graphs
copy_graphs:
	@echo "  COPY graphs"
	@$(foreach file,$(wildcard ../simulation/*graph.tex),$(call tail_copy,$(file),10))

Final-Paper.pdf: copy_graphs

# Clean rule to remove intermediates 
# produced by LaTeX and relevant libraries
.PHONY: clean
clean:
	@echo " CLEAN documentation"
	@rm -f *.pdf*
	@rm -f *.log
	@rm -f *.out
	@rm -f *.aux
	@rm -f *.blg
	@rm -f *.bbl
	@rm -f *.pyg
	@rm -rf _minted-*
