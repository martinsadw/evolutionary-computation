export IRACE_HOME=/usr/local/lib/R/site-library/irace
export PATH=${IRACE_HOME}/bin/:$PATH

irace -s /evolutionary-computation/irace/ga/scenario.txt > results/irace_ga_output.txt
