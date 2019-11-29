export IRACE_HOME=/usr/local/lib/R/site-library/irace
export PATH=${IRACE_HOME}/bin/:$PATH

irace -s /evolutionary-computation/irace/pso/scenario.txt > output.txt
