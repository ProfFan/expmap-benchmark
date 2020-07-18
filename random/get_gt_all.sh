#!/bin/zsh

foreach gtsam_conf ('full'); do
    echo "Benchmarking on ${gtsam_conf}"
    for i in ./gtruth/*; do
        filename=$(basename $i)
        dsname="${filename%.*}"
        echo "Processing ${dsname}"
         ./Pose3SLAM_getError.py -i ./gtruth/${dsname}.g2o 
    done
done