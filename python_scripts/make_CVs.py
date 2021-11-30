import numpy as np
import sys, os

os.chdir("/gpfs/alpine/bip109/scratch/agp2004/Maggie")

start = int(sys.argv[1])
stop = int(sys.argv[2])

print("start:", start)
print("stop:", stop)

check = np.load("numpy_files/check.npy", allow_pickle=True)
data_HL = np.load("numpy_files/raw_data_HL.npy")
data_NHL = np.load("numpy_files/raw_data_NHL.npy")
nhl_labels = np.load("numpy_files/nhl_labels.npy")
hl_labels = np.load("numpy_files/hl_labels.npy")
atom_resids = np.load("numpy_files/atom_resids.npy")
atom_names = np.load("numpy_files/atom_names.npy", allow_pickle=True)
rosetta_stone = np.load("numpy_files/rosetta_stone.npy")
pairs = np.load("numpy_files/pairs.npy")

HL_features = np.array([np.linalg.norm((data_HL[:,:,pair[0],:]-data_HL[:,:,pair[1],:]), axis=2) for pair in pairs[start:stop,:]]).transpose(1,2,0)

NHL_features = np.array([np.linalg.norm((data_NHL[:,:,pair[0],:]-data_NHL[:,:,pair[1],:]), axis=2) for pair in pairs[start:stop,:]]).transpose(1,2,0)

rosetta_stone = np.asarray([(atom_resids[pair[0]], atom_names[pair[0]], atom_resids[pair[1]], atom_names[pair[1]]) for pair in pairs[start:stop,:]])


filename = 'data/HL_' + str(start)
np.save(filename, HL_features)

filename = 'data/NHL_' + str(start)
np.save(filename, NHL_features)

filename = 'data/RS_' + str(start)
np.save(filename, rosetta_stone)

