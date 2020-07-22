#!/usr/bin/env python3
"""
 * @file Pose3SLAMExample_initializePose3.cpp
 * @brief A 3D Pose SLAM example that reads input from g2o, and initializes the
 *  Pose3 using InitializePose3
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
parser.add_argument('-i', '--input', help='input file g2o format', required=True)
args = parser.parse_args()

g2oFile = args.input

is3D = True
graph_in, initial = gtsam.readG2o(g2oFile, is3D)

graph = gtsam.NonlinearFactorGraph()
for i in range(graph_in.size()):
    factor = gtsam.dynamic_cast_BetweenFactorPose3_NonlinearFactor(graph_in.at(i))
    model = gtsam.noiseModel_Isotropic.Sigma(
            6, 1.0)
    graph.add(gtsam.BetweenFactorPose3(factor.keys().at(0), factor.keys().at(1), factor.measured(), model))

# Add Prior on the first key
priorModel = gtsam.noiseModel_Diagonal.Variances(vector6(1, 1, 1,
                                                         1, 1, 1))
firstKey = initial.keys().at(0)
graph.add(gtsam.PriorFactorPose3(firstKey, gtsam.Pose3(), priorModel))

print("", graph.error(initial))