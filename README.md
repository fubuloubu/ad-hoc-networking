# Ad-Hoc Networking Paper
Explore the considerations of number of end users to ad-hoc networking effectiveness

# Instructions
Review Documentation in *documentation* directory

To replicate experiments, use the following commands in the *simulation* directory:
~~~~bash
make -j[N] all
~~~~

where [N] is the number of processes you would like to dedicate to the simulation
(Reccomended is 2x number of CPU Cores)

To clean up all artifacts, run:
~~~~bash
make all-clean
~~~~
