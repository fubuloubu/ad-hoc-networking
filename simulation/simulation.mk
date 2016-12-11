# View user graphs
.PHONY: %-view
%-view: %.ul
	@echo "  VIEW $^"
	@./userlist.py -F $^ --show-usergraph 2> /dev/null

# Create user graphs
%-usergraph.tex: %.ul
	@echo " GRAPH $^"
	@./userlist.py -F $^ --print-usergraph
	@mv output-graph.tex $@

# Clean up simulation
.PHONY: clean
clean:
	@echo " CLEAN simulation"
	@rm -rf __pycache__
	@rm -f *.pyc
