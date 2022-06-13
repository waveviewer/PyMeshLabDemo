import argparse
import logging
import os.path
import time

import pymeshlab

parser = argparse.ArgumentParser(description='Simplify trimesh by MeshLab')
parser.add_argument('-i', '--input', help="input mesh file", required=True)
parser.add_argument('-o', '--output', help="save output filepath, support .obj, .ply", required=True)
parser.add_argument('-r', '--ratio', help="target percentage", default=0.1, type=float)
args = parser.parse_args()

if not os.path.exists(args.input):
    print("Can not open mesh file : ", args.input)
    exit(-1)

meshname = os.path.basename(args.input)
logger = logging.getLogger(meshname)
time_now = time.strftime("%Y%m%d", time.localtime())
logger_dir = "simplify_logs"
if not os.path.isdir(logger_dir):
    os.mkdir(logger_dir)
logger_filename = "{}/{}_{}.log".format(logger_dir, time_now, meshname)
ch = logging.FileHandler(filename=logger_filename, encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

ms = pymeshlab.MeshSet()
ms.load_new_mesh(args.input)
ms.set_current_mesh(0)
logger.info("load mesh {}".format(args.input))

logger.info("simplify ratio is {}".format(args.ratio))
start = time.perf_counter_ns()
ms.meshing_decimation_quadric_edge_collapse(targetperc=args.ratio)
end = time.perf_counter_ns()
print("time used {} ms".format((end-start)/1000/1000))
logger.info("meshing_decimation_quadric_edge_collapse time used {} ms".format((end-start)/1000/1000))

ms.save_current_mesh(args.output)
print("save result in {}".format(args.output))
logger.info("save result in {}".format(args.output))
