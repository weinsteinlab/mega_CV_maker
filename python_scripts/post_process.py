import numpy as np
import pickle
import os
import sys
import glob

os.chdir("/gpfs/alpine/bip109/scratch/agp2004/mega_CV_maker")

nhl_labels = np.load("numpy_files/nhl_labels.npy")
hl_labels = np.load("numpy_files/hl_labels.npy")

excluded = np.concatenate((np.arange(0,87), np.arange(272,312))).tolist()

feature_temp = []
for file in glob.glob("output/*.txt"):
    pickleFile = open(file, 'rb')
    temp = pickle.load(pickleFile)
    if temp:
        feature_temp.extend([x for x in temp if ((int(x[3][0]) not in excluded) and (int(x[3][2]) not in excluded))])

print("total number of features:", len(feature_temp), flush=True)

lig="LSD"
index1 = [i for i,y in enumerate([x[0] for x in feature_temp[0][4]]) if y==lig][0]
feature_list = [x for x in feature_temp if x[4][index1][1]==True]
print("number of LSD features:", len(feature_list), flush=True)

lig="MES"
index2 = [i for i,y in enumerate([x[0] for x in feature_temp[0][4]]) if y==lig][0]
feature_list = [x for x in feature_temp if x[4][index2][1]==True]
print("number of MES features:", len(feature_list), flush=True)

lig="DMT"
index3 = [i for i,y in enumerate([x[0] for x in feature_temp[0][4]]) if y==lig][0]
feature_list = [x for x in feature_temp if x[4][index3][1]==True]
print("number of DMT features:", len(feature_list), flush=True)

lig="DOI"
index4 = [i for i,y in enumerate([x[0] for x in feature_temp[0][4]]) if y==lig][0]
feature_list = [x for x in feature_temp if x[4][index4][1]==True]
print("number of DOI features:", len(feature_list), flush=True)

feature_list = [x for x in feature_temp if (x[4][index1][1]==True and x[4][index2][1]==True and x[4][index3][1]==True and x[4][index4][1]==True)]
print("total number of features overlapping LSD and DOI and DMT and MES", len(feature_list), flush=True)


filename = "all_overlap_features.txt"
with open(filename, "wb") as fp:
    pickle.dump(feature_list, fp)
