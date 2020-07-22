#!/bin/zsh

foreach gtsam_conf ('full' 'quat' 'default' 'rot3'); do
    #echo "{ \"${gtsam_conf}\": {"
    pip uninstall -q -y gtsam && pip install -q ../../packages/${gtsam_conf}/gtsam-4.0.2-cp38-cp38-manylinux2014_x86_64.whl
#    foreach i ('cubicle' 'garage' 'rim' 'sphere' 'torus3D'); do
    #python ./Error_Model.py
    ./get_gt_all.sh
    echo "}, "
done