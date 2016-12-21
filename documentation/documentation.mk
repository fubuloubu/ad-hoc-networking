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

# This is to remove extra instructions from matplotlib2tikz
tail_copy=tail -n +$(2) $(1) > $(shell basename $(1))

SIMGRAPHS=$(wildcard ../simulation/*-graph.tex) \
		  ../simulation/sim-usergraph.tex

.PHONY: copy_results
copy_results: $(SIMGRAPHS)
	@echo "  COPY results"
	@$(foreach file,$^,$(call tail_copy,$(file),10);)

$(SIMGRAPHS):
	@cd ../simulation && $(MAKE) -j4 all

%.tex.bak: %.tex
	@echo "SPLCHK $<"
	@aspell check $<
REPORT_SECTIONS=abstract.tex background.tex \
	     methodology.tex results.tex conclusion.tex

Final-Report.pdf: copy_results $(addsuffix .bak,$(REPORT_SECTIONS))
Final-Presentation.pdf: copy_results

# Clean rule to remove intermediates 
# produced by LaTeX and relevant libraries
.PHONY: clean
clean:
	@echo " CLEAN documentation"
	@grep -v "#\|^\$$" .gitignore | while read line; do rm -rf $$line; done
