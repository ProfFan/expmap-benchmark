#!/bin/bash

set -e

EXPERIMENT_NAME=$1
SWIFTFUSION_DIR="../SwiftFusion/SwiftFusion"

if [ "$EXPERIMENT_NAME" == "" ]; then
echo "Must have experiment name"
exit 1
fi

pids=""
echo "Experiment: $EXPERIMENT_NAME"
for dataset in ./datasets/*; do
    dsname=$(basename "$dataset" .g2o)
    echo "Processing: $dsname"
    mkdir -p "logs/${EXPERIMENT_NAME}_$dsname"
    echo "Executing"
    #python3 ./Pose3SLAMExample_g2o.py -i $dataset -o "results/$EXPERIMENT_NAME-$dsname.csv" -l "logs" -e "$EXPERIMENT_NAME" &
    $SWIFTFUSION_DIR/.build/release/Pose3SLAMG2O "$dataset" "results/$EXPERIMENT_NAME-$dsname.txt" -l "logs/${EXPERIMENT_NAME}_$dsname" --chordal &
    pids="$pids $!"
done

# wait for all pids
wait $pids
