import MDAnalysis
import numpy as np
import sys
import glob, os

os.chdir("/gpfs/alpine/bip109/proj-shared/mega_CV_maker")

u = MDAnalysis.Universe('trajectories/apo/prot.psf', 'trajectories/apo/trajectory_prot_0.xtc')

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

np.save('numpy_files/check', protein.atoms.names)

print(np.load('numpy_files/check.npy', allow_pickle=True))

