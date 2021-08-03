#!/bin/bash

export IRACE_HOME=/home/thales/R/x86_64-pc-linux-gnu-library/3.6/irace
export PATH=${IRACE_HOME}/bin/:$PATH
export PYTHONPATH=/mnt/c/Users/fonse/Documents/Improving-LOR

now="$(date +'%d-%m-%Y_%Hh-%Mm-%Ss')"

irace -s /mnt/c/Users/fonse/Documents/improving-LOR/irace/grasp/scenario.txt > /mnt/c/Users/fonse/Documents/improving-LOR/results/irace/irace_grasp_output_${now}.txt
