import numpy as np
import pickle
import os
import sys
import glob

os.chdir("/gpfs/alpine/bip109/scratch/agp2004/mega_CV_maker")

################
rez_map = []
for i in np.arange(60,86):
    rez_map.append((i, "TM1_extra"))

for i in np.arange(86,103):
    rez_map.append((i, "TM1_intra"))

for i in np.arange(103,107):
    rez_map.append((i, "ICL1"))

for i in np.arange(107,124):
    rez_map.append((i, "TM2_intra"))

for i in np.arange(124,139):
    rez_map.append((i, "TM2_extra"))

for i in np.arange(139,144):
    rez_map.append((i, "ECL1"))

for i in np.arange(144,161):
    rez_map.append((i, "TM3_extra"))

for i in np.arange(161,179):
    rez_map.append((i, "TM3_intra"))

for i in np.arange(179,188):
    rez_map.append((i, "ICL2"))

for i in np.arange(188,205):
    rez_map.append((i, "TM4_intra"))

for i in np.arange(205,218):
    rez_map.append((i, "TM4_extra"))

for i in np.arange(218,231):
    rez_map.append((i, "ECL2"))

for i in np.arange(231,249):
    rez_map.append((i, "TM5_extra"))

for i in np.arange(249,272):
    rez_map.append((i, "TM5_intra"))

for i in np.arange(272,312):
    rez_map.append((i, "ICL3"))

for i in np.arange(312,333):
    rez_map.append((i, "TM6_intra"))

for i in np.arange(333,350):
    rez_map.append((i, "TM6_extra"))

for i in np.arange(350,354):
    rez_map.append((i, "ECL3"))

for i in np.arange(354,368):
    rez_map.append((i, "TM7_extra"))

for i in np.arange(368,384):
    rez_map.append((i, "TM7_intra"))

for i in np.arange(384,420):
    rez_map.append((i, "H8"))
###############

def is_in_SMs(q, sm1, sm2):
    temp_string1 = [x[1] for x in rez_map if x[0]==int(q[0])][0]
    temp_string2 = [x[1] for x in rez_map if x[0]==int(q[2])][0]
    return ((sm1, sm2)==(temp_string1, temp_string2) or (sm1, sm2)==(temp_string2, temp_string2))

feature_temp = []
for file in glob.glob("output/*.txt"):
    pickleFile = open(file, 'rb')
    temp = pickle.load(pickleFile)
    if temp:
        feature_temp.extend([x for x in temp if is_in_SMs(x, 'TM4_extra', 'TM6_extra')])

print("total number of features:", len(feature_temp), flush=True)

filename = "TM4_extra_TM6_extra_features.txt"
with open(filename, "wb") as fp:
    pickle.dump(feature_list, fp)
