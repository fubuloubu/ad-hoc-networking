# View user graphs
.PHONY: %-view
%-view: %.ul
	@echo "  VIEW $^"
	@./userlist.py -F $^ --show-usergraph 2> /dev/null

# Print user graphs
%-usergraph.tex: %.ul
	@echo " GRAPH $^"
	@./userlist.py -F $^ --print-usergraph
	@mv output-graph.tex $@

# Run simulations
# NOTE: if %.args file exist, run N simulations
# using arguments from the file, 1 sim per line
%.results: %.ul
	@echo "   RUN $^"
	@if [ -e $*.args ] ; then \
	 	while read -r line; \
			do ./simulation.py $$line -F $^ >> $@ ; \
	 	done < $*.args ; \
	 else \
	 	./simulation.py -F $^ >> $@ ; \
	 fi

# Process results
%-results.tex: %.results
	@echo "   GEN $@"
	@./simulation_results_parser.py -t $^ > $@

.PHONY: all-results
all-results: $(patsubst %.ul,%.results,$(wildcard sims/*.ul))

# Clean up simulation
.PHONY: clean
clean:
	@echo " CLEAN simulation"
	@rm -rf __pycache__
	@rm -f *.pyc
