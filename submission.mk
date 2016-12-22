# Rules for making submission
DOCDIR=documentation
SIMDIR=simulation
DOCUMENTS=Final-Report.pdf Final-Presentation.pdf
SUBMISSION=../bje2113-e6950-final-project.zip
$(SUBMISSION):
	@echo "Preparing Submission..."
	@cd $(SIMDIR) && $(MAKE) -s all-clean
	@cd $(DOCDIR) && $(MAKE) -s clean $(DOCUMENTS)
	@echo "Zipping Submission..."
	@zip -q    $@ README.md
	@zip -q    $@ $(foreach doc,$(DOCUMENTS),$(DOCDIR)/$(doc)) 
	@zip -q -r $@ $(SIMDIR)
	@zip -q -d $@ $(SIMDIR)/.gitignore

zip-clean:
	@echo "Removing Submission..."
	@rm -f $(SUBMISSION)

# Shortcut so we don't have to type out the filename
.PHONY: submission
submission: zip-clean $(SUBMISSION)
