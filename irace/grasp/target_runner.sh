#!/bin/bash

EXE=/mnt/c/Users/fonse/Documents/improving-LOR/algorithms/grasp.py


CONFIG_ID=$1
INSTANCE_ID=$2
SEED=$3
INSTANCE=$4

shift 4 || exit 1
CONFIG_PARAMS=$*

LOGS=c${CONFIG_ID}-${INSTANCE_ID}.log
DAT_FILE=c${CONFIG_ID}-${INSTANCE_ID}.dat
touch ${DAT_FILE}

python3 $EXE -v ${CONFIG_PARAMS} --datfile ${DAT_FILE} > ${LOGS} 2>&1

error() {
    echo "`TZ=UTC date`: error: $@"
    exit 1
}

# This is an example of reading a number from the output.
# It assumes that the objective value is the first number in
# the first column of the last line of the output.
if [ -s "${DAT_FILE}" ]; then
	COST=$(cat "${DAT_FILE}" | grep -e '^[0-9]' | cut -f1)
	# use echo "-$COST" to
	# Negative because score is maximised but irace minimises.
    echo "$COST"
    rm -f "${LOGS}" "${DAT_FILE}" 
    exit 0
else
    error "${DAT_FILE}: No such file or directory"
fi