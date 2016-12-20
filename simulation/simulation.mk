IGNORE_WARNINGS=2>/dev/null

# Directory to hold simulation results
SIMDIR=sims
SIMPREFIX=sim
$(SIMDIR):
	@echo " MKDIR $@"
	@mkdir $@;

# Generate userlist 
# Parse file name like /dir/../dir/sim-aNUM-bNUM-c...*.ul
# into flags for executable
GET_SIM_ARGS_FROM_FILE=$(subst -, -,$(subst $(SIMPREFIX),,$(basename $(notdir $(1)))))
%.ul: | $(SIMDIR)
	@echo "   GEN $@"
	@./userlist.py $(call GET_SIM_ARGS_FROM_FILE,$@) >$@ $(IGNORE_WARNINGS)

# View user graphs
# (FOR DEBUG ONLY)
.PHONY: %-view
%-view: %.ul
	@echo "  VIEW $^"
	@./userlist.py -f $^ --show-usergraph $(IGNORE_WARNINGS)

# Print user graphs
%-usergraph.tex: %.ul
	@echo " GRAPH $@"
	@./userlist.py -f $^ --print-usergraph >$@ $(IGNORE_WARNINGS)

# Experiments
varA= 10  12  15  20  25  30  40  50  60  80  100  120  160
varR= 10  12  15  20  25  30  40  50  60  80  100  120  160
varU=100 120 150 200 250 300 400 500 600 800 1000 1200 1600
# This one must be handled separately
# because it's not in the userlist
varI=0.010 0.012 0.015 0.020 0.030 0.040 0.060 0.080 0.100

USERLIST_FILENAME=$(addsuffix .ul,$(addprefix $(SIMDIR)/$(SIMPREFIX),$(1)))
varA_USERLISTS=$(foreach arg,$(varA),$(call USERLIST_FILENAME,-x$(arg)-y$(arg)))
varR_USERLISTS=$(foreach arg,$(varR),$(call USERLIST_FILENAME,-r$(arg)))
varU_USERLISTS=$(foreach arg,$(varU),$(call USERLIST_FILENAME,-u$(arg)))
varI_USERLISTS=$(SIMDIR)/$(SIMPREFIX).ul

varI_ARGS=$(subst .ul,.args,$(varI_USERLISTS))
$(varI_ARGS): | $(SIMDIR)
	@echo "   GEN $@"
	@$(foreach intensity,$(varI),$(shell echo "-i $(intensity)" >> $@;))

# This is done so we generate the args file for the intensity experiment
$(varI_USERLISTS): $(varI_ARGS)

ALL_USERLISTS=$(varA_USERLISTS) $(varR_USERLISTS) $(varU_USERLISTS) $(varI_USERLISTS)

.PHONY: all-userlists
all-userlists: $(ALL_USERLISTS)

# Run simulations
# NOTE: if %.args file exist, run N simulations
# using arguments from the file, 1 sim per line
%.results: %.ul
	@echo "   RUN $^"
	@if [ -e $*.args ] ; then \
	 	while read -r line; \
			do ./simulation.py $$line -f $^ >>$@ $(IGNORE_WARNINGS); \
	 	done < $*.args ; \
	 else \
	 	./simulation.py -f $^ >> $@ $(IGNORE_WARNINGS); \
	 fi
	@# Technically it is created above, 
	@# but for completeness...
	@echo "   GEN $@"

varA_RESULTS=$(subst .ul,.results,$(varA_USERLISTS))
varR_RESULTS=$(subst .ul,.results,$(varR_USERLISTS))
varU_RESULTS=$(subst .ul,.results,$(varU_USERLISTS))
varI_RESULTS=$(subst .ul,.results,$(varI_USERLISTS))
.PHONY: all-results
all-results: $(subst .ul,.results,$(ALL_USERLISTS))

# Process results
# (FOR DEBUG ONLY)
%-results.tex: %.results
	@echo "   GEN $@"
	@./simulation_results_parser.py -t $^ >$@

# Helper to get middle part of a filename, which will contain metric to graph
GET_METRIC=$(shell echo $(1) | sed "s/[[:lower:]]*-\(.*\)-$(2).tex/\1/")

%-graph.tex:
	@echo "   GEN $@"
	@./simulation_results_parser.py \
		-m avg-$(call GET_METRIC,$@,graph) \
		-r \
		sims/sim "" \
		.results "" \
		+x "" \
		+y x \
		+r "" \
		+u "" \
		-g $^ >$@

varA_GRAPHS=vararea-average-latency-graph.tex vararea-success-rate-graph.tex
$(varA_GRAPHS): $(varA_RESULTS)
varR_GRAPHS=varradius-average-latency-graph.tex varradius-success-rate-graph.tex
$(varR_GRAPHS): $(varR_RESULTS)
varU_GRAPHS=varusers-average-latency-graph.tex varusers-success-rate-graph.tex
$(varU_GRAPHS): $(varU_RESULTS)

# Handle this one separately because of metric location
varI_TABLES=varintensity-average-latency-table.tex varintensity-success-rate-table.tex
$(varI_TABLES): $(varI_RESULTS)
	@echo "   GEN $@"
	@./simulation_results_parser.py \
		-m $(call GET_METRIC,$@,table)-[0-9]* \
		-f latex \
		-t $^ >$@

ALL_ITEMS=$(varA_GRAPHS) $(varR_GRAPHS) $(varU_GRAPHS) $(varI_TABLES)

.PHONY: all
all: $(ALL_ITEMS) $(SIMDIR)/$(SIMPREFIX)-usergraph.tex
	@# Move this at the end so documentation can copy all at once
	@echo "  MOVE $(SIMPREFIX)-usergraph.tex"
	@mv $(SIMDIR)/$(SIMPREFIX)-usergraph.tex $(SIMPREFIX)-usergraph.tex

# Clean up simulation
.PHONY: clean
clean:
	@echo " CLEAN simulation"
	@rm -rf __pycache__
	@rm -f *.pyc
	@rm -f  $(ALL_ITEMS)
	@rm -f  $(SIMPREFIX)-usergraph.tex
	@rm -rf $(SIMDIR)
