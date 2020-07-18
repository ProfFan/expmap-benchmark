#!/bin/zsh

foreach gtsam_conf ('full' 'quat' 'default' 'rot3'); do
    echo "Benchmarking on ${gtsam_conf}"
    pip uninstall -y gtsam && pip install ../packages/${gtsam_conf}/gtsam-4.0.2-cp38-cp38-manylinux2014_x86_64.whl
#    foreach i ('cubicle' 'garage' 'rim' 'sphere' 'torus3D'); do
    foreach i ('grid3D'); do
        filename=$(basename $i)
        #dsname="${filename%.*}"
        dsname=$i
        echo "Processing ${dsname}"
        ./randomized_bench.sh ${gtsam_conf} ${dsname}
    done
done