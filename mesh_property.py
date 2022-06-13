import os
import time

import pymeshlab
import argparse
import logging

parser = argparse.ArgumentParser(description='Print mesh properties, logs saved')
parser.add_argument('-i', '--input', help="input mesh file", required=True)
parser.add_argument('-c', '--compare', help="the compared mesh to get hausdorff distance")
args = parser.parse_args()

ms = pymeshlab.MeshSet()
logger_dir = "property_logs"
if not os.path.isdir(logger_dir):
    os.mkdir(logger_dir)

# check input
if not os.path.exists(args.input):
    print("Can not open file ", args.input)
    exit(-1)
else:
    meshname = os.path.basename(args.input)
    meshpath = args.input
    ms.load_new_mesh(meshpath)
    print("get input mesh: ", meshpath)

if args.compare:
    if os.path.exists(args.compare):
        compared_mesh_path = args.compare
        ms.load_new_mesh(compared_mesh_path)
        print("get compared mesh: ", compared_mesh_path)
    else:
        print("Can not open file ", args.compare)
        exit(-1)

# init logger
logger = logging.getLogger(meshname)
time_now = time.strftime("%Y%m%d", time.localtime())
logger_filename = "{}/{}_{}.log".format(logger_dir, time_now, meshname)
ch = logging.FileHandler(filename=logger_filename, encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)


ms.set_current_mesh(0)
topo_info = ms.get_topological_measures()
logger.info("Mesh name is {}".format(meshname))
logger.info("vertices_number : {} , edges_number : {} , faces_number : {}".format(
    topo_info["vertices_number"], topo_info["edges_number"], topo_info["faces_number"]))
logger.info("boundary_edges : {}".format(topo_info["boundary_edges"]))
logger.info("connected_components_number : {}".format(topo_info["connected_components_number"]))
logger.info("genus : {}".format(topo_info["genus"]))
logger.info("unreferenced_vertices : {}".format(topo_info["unreferenced_vertices"]))

logger.info("is_mesh_two_manifold : {}".format(topo_info["is_mesh_two_manifold"]))
if not topo_info["is_mesh_two_manifold"]:
    logger.info(
        "non_two_manifold_edges : {}".format(topo_info["non_two_manifold_edges"]))
    logger.info(
        "non_two_manifold_vertices : {}".format(topo_info["non_two_manifold_vertices"]))
    logger.info(
        "incident_faces_on_non_two_manifold_edges : {}".format(topo_info["incident_faces_on_non_two_manifold_edges"]))
    logger.info(
        "incident_faces_on_non_two_manifold_vertices : {}".format(topo_info["incident_faces_on_non_two_manifold_vertices"]))

for key,value in topo_info.items():
    print("{} : {}".format(key, value))


if args.compare:
    distance = ms.get_hausdorff_distance(sampledmesh=0, targetmesh=1)
    logger.info("Compute hausdorff_distance")
    logger.info("sampled mesh is {}".format(meshpath))
    logger.info("target mesh is {}".format(compared_mesh_path))
    for key,value in distance.items():
        print("{} : {}".format(key, value))
        logger.info("{} : {}".format(key, value))
