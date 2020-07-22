#!/usr/bin/env python3
"""
 * @file Error_Model.py
 * @brief see how error model change with expmap
 * @date Jan 17, 2019
 * @author Vikrant Shah based on CPP example by Luca Carlone
"""
# pylint: disable=invalid-name, E1101

from __future__ import print_function
import argparse
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import gtsam
from gtsam.utils import plot
from gtsam.utils.logging_optimizer import gtsam_optimize

import tensorboardX
from tensorboardX import SummaryWriter

def vector6(x, y, z, a, b, c):
    """Create 6d double numpy array."""
    return np.array([x, y, z, a, b, c], dtype=np.float)


parser = argparse.ArgumentParser(
    description="A 3D Pose SLAM example that reads input from g2o, and "
                "initializes Pose3")
parser.add_argument('-i', '--input', help='input file g2o format', required=False)
args = parser.parse_args()

graph = gtsam.NonlinearFactorGraph()

# for i in range(graph_in.size()):
measurement = gtsam.Pose3(gtsam.Rot3.RzRyRx(1, 1, 1), gtsam.Point3(1, 1, 1))
model = gtsam.noiseModel_Isotropic.Sigma(
        6, 1.0)
factor = gtsam.BetweenFactorPose3(0, 1, measurement, model)

graph.add(factor)

# Add Prior on the first key
# priorModel = gtsam.noiseModel_Diagonal.Variances(vector6(1, 1, 1,
#                                                          1, 1, 1))
# firstKey = initial.keys().at(0)
# graph.add(gtsam.PriorFactorPose3(firstKey, gtsam.Pose3(), priorModel))
val = gtsam.Values()
val.insert(0, gtsam.Pose3.identity())
val.insert(1, gtsam.Pose3.identity())

def linearize(graph, val) -> gtsam.GaussianFactorGraph:
    return graph.linearize(val)

print("error vector = ", linearize(graph, val).augmentedJacobian()[:, -1])
print("initial error = ", graph.error(val))