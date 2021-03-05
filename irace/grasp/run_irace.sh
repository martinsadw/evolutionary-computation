#!/bin/bash

export IRACE_HOME=/home/bravo/R/x86_64-pc-linux-gnu-library/3.6/irace
export PATH=${IRACE_HOME}/bin/:$PATH

now="$(date +'%d-%m-%Y_%Hh-%Mm-%Ss')"

irace -s /mnt/c/Users/natal/Documents/Natalie/TCC/improving-LOR/irace/grasp/scenario.txt > /mnt/c/Users/natal/Documents/Natalie/TCC/improving-LOR/results/irace/irace_grasp_output_${now}.txt
