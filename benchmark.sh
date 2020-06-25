#!/bin/bash

set -e

EXPERIMENT_NAME=$1

if [ "$EXPERIMENT_NAME" == "" ]; then
echo "Must have experiment name"
exit 1
fi

pids=""
echo "Experiment: $EXPERIMENT_NAME"
for dataset in ./datasets/*; do
    dsname=$(basename "$dataset" .g2o)
    echo "Processing: $dsname"
    echo "Executing: python3 ./Pose3SLAMExample_g2o.py -i $dataset -o \"results/$EXPERIMENT_NAME-$dsname.csv\" -l \"logs\" -e \"$EXPERIMENT_NAME\""
    python3 ./Pose3SLAMExample_g2o.py -i $dataset -o "results/$EXPERIMENT_NAME-$dsname.csv" -l "logs" -e "$EXPERIMENT_NAME" &
    pids="$pids $!"
done

# wait for all pids
wait $pids
