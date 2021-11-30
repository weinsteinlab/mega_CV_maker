import numpy as np
import pickle
import os
import sys

os.chdir("/gpfs/alpine/bip109/scratch/agp2004/Maggie")

start = sys.argv[1] # unique key to point to data file to analyze (had to split data into many files because was >3TB)


nhl_labels = np.load("numpy_files/nhl_labels.npy") # key for indices of the 23 hallucinogen trajectories (5HT_0, 5HT_1, etc)
hl_labels = np.load("numpy_files/hl_labels.npy") # key for non-hallucinogen trajectories (LSD_0, LSD_1, etc)

HL_features = np.load("data/HL_" + start + ".npy") # hallucinogen distance matrix, shape (trajectories, frames, distances)
NHL_features = np.load("data/NHL_" + start + ".npy") # non-hallucinogen distance matrix, shape (trajectories, frames, distances)
rosetta_stone = np.load("data/RS_" + start + ".npy") # key to translate which residues/atoms cooresponds to each distance

hall_ligs = ["apo"] # hallucinogen systems
nhall_ligs = ["cara"] # non-hallucinogen systems

max_nhall_prob = 0.1 # maximum state probability for non-hallucinogens. Each ligand-system should not sample more than this fraction
min_hall_prob = 0.40 # minimum state probability for hallucinogens. Each ligand-system should sample at least this fraction
first_frame=1000      # option to skip some number of frames

feature_list=[]
hit_list=[]
for feature in range(NHL_features.shape[2]): # loop over distances
    maxx = NHL_features[:,:,feature].flatten().max()
    minn = NHL_features[:,:,feature].flatten().min()
    NHL=[]
    HL=[]
    for threshold in np.linspace(minn,maxx,16): # sweep 15 thresholds across the min/max of Nhall values for the distance
        nhl_temp=[]
        for lig in nhall_ligs:
            temp=[]
            ind = np.squeeze(np.asarray([i for i, v in enumerate(nhl_labels) if lig in v])) # trajectory indices for the lig
            try:
                for i in ind:
                    temp.append(NHL_features[i,first_frame:,feature])
            except:
                temp.append(NHL_features[ind,first_frame:,feature])
            temp=np.asarray(temp)
            nhl_temp.append((lig,(temp.flatten()>threshold).mean())) # fraction of the frames above the threshold

        hl_temp=[]
        for lig in hall_ligs:
            temp=[]
            ind = np.squeeze(np.asarray([i for i, v in enumerate(hl_labels) if lig in v]))
            try:
                for i in ind:
                    temp.append(HL_features[i,first_frame:,feature])
            except:
                temp.append(HL_features[ind,first_frame:,feature])
            temp=np.asarray(temp)
            hl_temp.append((lig,(temp.flatten()>threshold).mean()))
        NHL.append(nhl_temp)
        HL.append(hl_temp)
        
    NHL=np.asarray(NHL).transpose(1,0,2) # transpose (thresholds, ligands, fractions) to (ligands, thresholds, fractions) 
    HL=np.asarray(HL).transpose(1,0,2)

# --------------------------------------------------
# now apply filter on data gathered above to satisfy probability criteria. Searching for CVs that have values sampled by the non-hallucinogens less than X% of the time while these values are sampled by each hallucinogen system greater than y% of the time, on either side of the non-hallucinogen values

    hits=[]
    thresh=0              # initialize to prevent error if no hit found
    for x in HL:          # loop over ligands
        name = x[0][0]    # name of the ligand
        hit=False         # initialize as not a hit
        for i,q in enumerate(x):  # loop over the thresholds
            nhl_max = NHL[:,i,1].astype(np.float).max()   # maximum fraction sampled by the NHL systems at that threshold
            if np.logical_and(q[1].astype(np.float)>min_hall_prob,nhl_max<max_nhall_prob): 
                hit=True
                thresh = np.linspace(minn,maxx,16)[i]
            nhl_max = (1-NHL[:,i,1].astype(np.float)).max()   # using 1-fraction to get fraction sampled below threshold. Want to allow Halls to sample on either side of Nhall values (bigger or smaller distances than Nhalls)
            if np.logical_and((1-q[1].astype(np.float))>min_hall_prob,nhl_max<max_nhall_prob): 
                hit=True
                thresh = np.linspace(minn,maxx,16)[i]
        hits.append((name, hit, thresh))
    
    if sum([x[1] for x in hits])>0: # If at least 1 Hallucinogen passes criteria
        hit_list.append((feature, NHL_features[:,:,feature], HL_features[:,:,feature], rosetta_stone[feature], hits))
    
filename = "output/" + start + ".txt"
with open(filename, "wb") as fp:
    pickle.dump(hit_list, fp)
