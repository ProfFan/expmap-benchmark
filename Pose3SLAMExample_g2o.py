#!/usr/local/bin/python3
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
parser.add_argument('-o', '--output',
                    help="the path to the output file with optimized graph")
parser.add_argument("-p", "--plot", action="store_true",
                    help="Flag to plot results")
parser.add_argument('-l', '--logdir', help='where to store tensorboard log', required=True)
parser.add_argument('-e', '--prefix', help='log name prefix', required=True)
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

print("Adding prior to g2o file ")
firstKey = initial.keys().at(0)
graph.add(gtsam.PriorFactorPose3(firstKey, gtsam.Pose3(), priorModel))

params = gtsam.LevenbergMarquardtParams.CeresDefaults()
params.setMaxIterations(100)
params.setVerbosityLM("SUMMARY")  # this will show info about stopping conds
optimizer = gtsam.LevenbergMarquardtOptimizer(graph, initial, params)

import os
dsname=os.path.splitext(os.path.basename(g2oFile))[0]

print("Logging to: " + args.logdir + "/" + args.prefix + "_" + dsname)
writer = SummaryWriter(args.logdir + "/" + args.prefix + "_" + dsname)

def hook(optimizer, error: float):
    writer.add_scalar("optimizer/loss",
                        error, optimizer.iterations())
    writer.add_scalar("optimizer/lambda", optimizer.lambda_(), optimizer.iterations())
    writer.flush()

gtsam_optimize(optimizer, params, hook)

result = optimizer.values()

print("Optimization complete")

print("initial error = ", graph.error(initial))
print("final error = ", graph.error(result))

if args.output is None:
    print("Final Result:\n{}".format(result))
else:
    outputFile = args.output
    print("Writing results to file: ", outputFile)
    graphNoKernel, _ = gtsam.readG2o(g2oFile, is3D)
    gtsam.writeG2o(graphNoKernel, result, outputFile)
    print ("Done!")

if args.plot:
    resultPoses = gtsam.utilities_allPose3s(result)
    for i in range(resultPoses.size()):
        plot.plot_pose3(1, resultPoses.atPose3(i))
    plt.show()
