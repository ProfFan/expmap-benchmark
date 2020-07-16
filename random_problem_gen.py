#!/usr/local/bin/python3
"""
 * Generate random Pose3SLAM problem
"""
# pylint: disable=invalid-name, E1101

from __future__ import print_function
import argparse
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import gtsam

parser = argparse.ArgumentParser(
    description="A generator for random Pose3 problems")
parser.add_argument('-i', '--input', help="source g2o", required=True)
parser.add_argument('-o', '--output',
                    help="the path to the output file with randomized init", required=True)
args = parser.parse_args()

g2oFile = args.output
inputFile = args.input

import sys, os
sys.path.append(os.path.join(sys.path[0],'shonan', 'python'))

from random_pose_slam_problem import RandomPoseSLAMProblem
from sfm_problem import SFMProblem

# problem = RandomPoseSLAMProblem(nr_poses=1000, nr_measurements=1000, radius=10.0, sigma=0.8, model_sigma=1.0)
problem = lambda: None

input_graph, input_poses = gtsam.readG2o(inputFile, True)
problem._poses = input_poses
problem._graph = input_graph

from gtsam import writeG2o

def vector6(x, y, z, a, b, c):
    """Create 6d double numpy array."""
    return np.array([x, y, z, a, b, c], dtype=np.float)

poses = gtsam.Values()
graph = gtsam.NonlinearFactorGraph()
keys = problem._poses.keys()
import utils
for i in range(keys.size()):
    rand = utils.random_omega(100.0)
    randr = utils.random_omega(100.0)
    poses.insert(keys.at(i), gtsam.Pose3(gtsam.Rot3.RzRyRx(randr[0], randr[1],randr[2]), gtsam.Point3(rand[0], rand[1], rand[2])))

for i in range(problem._graph.size()):
    factor = gtsam.dynamic_cast_BetweenFactorPose3_NonlinearFactor(problem._graph.at(i))
    model = gtsam.noiseModel_Isotropic.Sigma(
            6, 1.0)
    graph.add(gtsam.BetweenFactorPose3(factor.keys().at(0), factor.keys().at(1), factor.measured(), model))
writeG2o(graph, poses, g2oFile)