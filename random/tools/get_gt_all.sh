#!/bin/zsh

foreach gtsam_conf ('full'); do
    echo " \"${gtsam_conf}\": {"
    for i in ../gtruth/*; do
        filename=$(basename $i)
        dsname="${filename%.*}"
        echo "\"${dsname}\": "
         ./Pose3SLAM_getError.py -i ../gtruth/${dsname}.g2o
        echo ","
    done
    echo "}"
done