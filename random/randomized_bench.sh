#!/bin/bash

set -e

EXPERIMENT_NAME=$1
DSNAME=$2

if [ "$EXPERIMENT_NAME" == "" ]; then
echo "Must have experiment name"
exit 1
fi

if [ "$DSNAME" == "" ]; then
echo "Must have dataset name"
exit 1
fi

pids=""
jobs=0
echo "Experiment: $EXPERIMENT_NAME"
for dataset in ./datasets/$DSNAME/*; do
    dsid=$(basename "$dataset" .g2o)
    echo "Processing: $DSNAME-$dsid"
    echo "Executing: python3 ../Pose3SLAMExample_g2o.py -i $dataset -o \"results/$EXPERIMENT_NAME-$DSNAME-$dsid.csv\" -l \"logs\" -e \"$EXPERIMENT_NAME-$DSNAME\""
    python3 ../Pose3SLAMExample_g2o.py -i $dataset -o "results/$EXPERIMENT_NAME-$DSNAME-$dsid.csv" -l "logs" -e "$EXPERIMENT_NAME-$DSNAME" &
    pids="$pids $!"
    jobs=$((jobs + 1))
    if [ $jobs -eq 4 ]; then
        wait $pids
        jobs=0
        pids=""
    fi
done
