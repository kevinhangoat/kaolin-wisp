import pickle
import pdb
import matplotlib.pyplot as plt

pkl_path = "/scratch_net/biwidl208/yuthan/wisp_data/nerf/d389c316-c71f7a5e/poses.pkl"
with open(pkl_path, "rb") as fid:
    poses = pickle.load(fid)

zdata = []
xdata = []
ydata = []
for pose in poses:
    zdata.append(pose[1])
    xdata.append(pose[0])
    ydata.append(pose[2])

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(xdata, ydata, zdata)

pdb.set_trace()