import MDAnalysis
import numpy as np
import sys
import glob, os

from itertools import combinations

os.chdir("/gpfs/alpine/bip109/scratch/agp2004/Maggie")

DATA_DIR = '/gpfs/alpine/bip109/scratch/agp2004/Maggie/trajectories/'

check = np.load("numpy_files/check.npy", allow_pickle=True)
print(check)

NHL_trajes = ["cara"]
HL_trajes = ["apo"]
start=0
end=3310
skip=1

data_HL = []
hl_labels=[]

for lig in HL_trajes:
    for i in range(19):
        temp=[]
        dcd = DATA_DIR + lig + "/trajectory_prot_" + str(i) + ".xtc"
        psf = DATA_DIR + lig + "/prot.psf"
        try:
            u = MDAnalysis.Universe(psf, dcd)
            print(lig, i, flush=True)
            #protein = u.select_atoms("protein and (prop mass>2)")
            protein = u.select_atoms("""protein and (
            (resname ALA and name C CA N O CB) or 
            (resname ARG and name C CA N O CZ) or
            (resname ASN and name C CA N O ND2 OD1) or
            (resname ASP and name C CA N O CG) or
            (resname CYS and name C CA N O SG) or
            (resname GLN and name C CA N O OE1 NE2) or
            (resname GLU and name C CA N O CD) or 
            (resname GLY and name C CA N O) or
            (resname HSE and name C CA N O ND1 NE2) or
            (resname ILE and name C CA N O CD CG2) or
            (resname LEU and name C CA O N CG) or
            (resname LYS and name C CA O N NZ) or
            (resname MET and name C CA O N SD) or
            (resname PHE and name C CA O N CG CZ) or
            (resname PRO and name C CA O N CG) or
            (resname SER and name C CA O N OG) or
            (resname THR and name C CA O N OG1 CG2) or
            (resname TRP and name C CA O N NE1 CZ3) or 
            (resname TYR and name C CA O N CG OH) or 
            (resname VAL and name C CA O N CB))""")


            if not np.array_equal(protein.atoms.names, check):
                raise Exception("non-conforming array")
            for ts in u.trajectory:
                temp.append(protein.positions)
            data_HL.append(np.array(temp)[start:end:skip])
            hl_labels.append(lig+"_"+str(i))
        except:
            print('no file for:', psf, dcd)
            continue

data_NHL=[]
nhl_labels=[]

for lig in NHL_trajes:
    for i in range(19):
        temp=[]
        dcd = DATA_DIR + lig + "/trajectory_prot_" + str(i) + ".xtc"
        psf = DATA_DIR + lig + "/prot.psf"
        try:
            u = MDAnalysis.Universe(psf, dcd)
            print(lig, i, flush=True)
            #protein = u.select_atoms("protein and (prop mass>2)")
            protein = u.select_atoms("""protein and (
            (resname ALA and name C CA N O CB) or 
            (resname ARG and name C CA N O CZ) or
            (resname ASN and name C CA N O ND2 OD1) or
            (resname ASP and name C CA N O CG) or
            (resname CYS and name C CA N O SG) or
            (resname GLN and name C CA N O OE1 NE2) or
            (resname GLU and name C CA N O CD) or 
            (resname GLY and name C CA N O) or
            (resname HSE and name C CA N O ND1 NE2) or
            (resname ILE and name C CA N O CD CG2) or
            (resname LEU and name C CA O N CG) or
            (resname LYS and name C CA O N NZ) or
            (resname MET and name C CA O N SD) or
            (resname PHE and name C CA O N CG CZ) or
            (resname PRO and name C CA O N CG) or
            (resname SER and name C CA O N OG) or
            (resname THR and name C CA O N OG1 CG2) or
            (resname TRP and name C CA O N NE1 CZ3) or 
            (resname TYR and name C CA O N CG OH) or 
            (resname VAL and name C CA O N CB))""")

            if not np.array_equal(protein.atoms.names, check):
                raise Exception("non-conforming array")
            for ts in u.trajectory:
                temp.append(protein.positions)
            data_NHL.append(np.array(temp)[start:end:skip])
            nhl_labels.append(lig+"_"+str(i))
        except:
            print('no file for:', psf, dcd)
            continue


data_HL = np.array(data_HL)
data_NHL = np.array(data_NHL)
hl_labels = np.array(hl_labels)
nhl_labels = np.array(nhl_labels)

atom_names = protein.atoms.names
atom_resids = protein.atoms.resids

Calphas = np.array(list(range(data_HL.shape[2])))

pairs = list(combinations(Calphas,2))

rosetta_stone = [(atom_resids[pair[0]], atom_names[pair[0]], atom_resids[pair[1]], atom_names[pair[1]]) for pair in pairs]

np.save("numpy_files/raw_data_HL.npy", data_HL)
np.save("numpy_files/raw_data_NHL.npy", data_NHL)
np.save("numpy_files/nhl_labels.npy", nhl_labels)
np.save("numpy_files/hl_labels.npy", hl_labels)
np.save("numpy_files/atom_resids.npy", protein.atoms.resids)
np.save("numpy_files/atom_names.npy", protein.atoms.names)
np.save("numpy_files/rosetta_stone.npy", np.asarray(rosetta_stone))
np.save("numpy_files/pairs.npy", np.asarray(pairs))
