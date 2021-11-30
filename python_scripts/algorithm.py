import numpy as np
import pickle
import os
import sys

os.chdir("/gpfs/alpine/bip109/scratch/agp2004/mega_CV_maker")

start = sys.argv[1]


nhl_labels = np.load("nhl_labels.npy")
hl_labels = np.load("hl_labels.npy")

HL_features = np.load("data/HL_" + start + ".npy")
NHL_features = np.load("data/NHL_" + start + ".npy")
rosetta_stone = np.load("data/RS_" + start + ".npy")

hall_ligs = ["LSD", "DOI", "DMT", "MES"]
nhall_ligs = ["5HT", "ERG", "LIS", "KET"]
first_frame=0
# filterz = extra_rezzes
filterz = np.arange(1000)

feature_list=[]
for feature in range(NHL_features.shape[2]):
    maxx = np.concatenate((HL_features[:,:,feature].flatten(), NHL_features[:,:,feature].flatten())).max()
    minn = np.concatenate((HL_features[:,:,feature].flatten(), NHL_features[:,:,feature].flatten())).min()
    for threshold in np.linspace(minn,maxx,16):
        NHL=[]
        for lig in nhall_ligs:
            temp=[]
            ind = np.squeeze(np.asarray([i for i, v in enumerate(nhl_labels) if lig in v]))
            for i in ind:
                temp.append(NHL_features[i,first_frame:,feature])
            temp=np.asarray(temp)
            NHL.append((lig,(temp.flatten()>threshold).mean()))

        HL=[]
        for lig in hall_ligs:
            temp=[]
            ind = np.squeeze(np.asarray([i for i, v in enumerate(hl_labels) if lig in v]))
            for i in ind:
                temp.append(HL_features[i,first_frame:,feature])
            temp=np.asarray(temp)
            HL.append((lig,(temp.flatten()>threshold).mean()))

        NHL=np.asarray(NHL)
        HL=np.asarray(HL)

        if np.logical_and((NHL[:,1].astype(np.float).max()<0.1), (HL[:,1].astype(np.float).min()>0.2)):
            if np.logical_and(int(rosetta_stone[feature][0]) in filterz, int(rosetta_stone[feature][2]) in filterz):
                check = np.abs(NHL[:,1].astype(np.float).mean()-HL[:,1].astype(np.float).mean())
                if check>0.0:
                    feature_list.append((feature, threshold, NHL_features[:,:,feature], HL_features[:,:,feature], rosetta_stone[feature]))
                    print("threshold: ", threshold)
                    print("feature: ", feature)
                    print("resids: ", rosetta_stone[feature])
                    print(NHL)
                    print(HL)

        if np.logical_and((HL[:,1].astype(np.float).max()<0.8), (NHL[:,1].astype(np.float).min()>0.90)):
            if np.logical_and(int(rosetta_stone[feature][0]) in filterz, int(rosetta_stone[feature][2]) in filterz):
                check = np.abs(NHL[:,1].astype(np.float).mean()-HL[:,1].astype(np.float).mean())
                if check>0.0:
                    feature_list.append((feature, threshold, NHL_features[:,:,feature], HL_features[:,:,feature], rosetta_stone[feature]))
                    print("threshold: ", threshold)
                    print("feature: ", feature)
                    print("resids: ", rosetta_stone[feature])
                    print(NHL)
                    print(HL)

filename = "output/" + start + ".txt"
with open(filename, "wb") as fp:
    pickle.dump(feature_list, fp)
