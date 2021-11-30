# mega_CV_maker
Algorithm to identify protein distances in MD simulations that differentiate classes of ensembles


Description:
Finds conformations (actually distances indicative of the conformations) visted by HL class that are not visited by NHL class using probability thresholds determined by the user


################################BUGS and TODO list################################
1) For some reason every time I activate conda, it edits the paths in the bashrc, breaking them. So in submit.sh I copy a fresh bashrc every time I need to activate a conda environment. I put this extra bashrc_copy in this folder.

2) If there is no lab environment with mdanalysis you might need to make your own with thee following commands:

	- cp ~/bashrc_copy ~/.bashrc
	- source ~/.bashrc
	- conda create -n md_analysis -y python=3.6
	- conda activate md_analysis
	- conda install -y -c conda-forge mdanalysis
	
If you get inconsistency warnings, I think we can cautiously ignore them. I have run the code without error despite these warnings.

3) I need to update algorithm to look for the opposite (visited by NHL class but not visited by HL class).

4) Current implementation doesn't allow the trajectories to have different number of frames (but different number of trajectories is fine).

DONE 5) Should use Shana's residue definitions to decrease size of output

6) Should follow Derek's suggestion to decrease number of floats stored by numpy. Don't need 32 decimals of angstrom precision...

7) Should change workflow to request many nodes for one job to get around the 4 jobs at a time limit on andes
#############################################################


###############TO RUN###############################

NOTE: The files are configured to run on andes, because it is free... The submit.sh must be edited to run on SUMMIT

1) place trajectories in 'trajectories' directory.

2) open python_scripts/check.py. edit the os.chdir() and the trajectory paths. You can use any trajectory. The point of this is to create a check.npy file containing the names of all of the atoms that will be used in the distance calculation. This file will be used to check the rest of the frames to ensure consistency in the next step.

3) open submit.sh and uncomment the '#python3 -u python_scripts/check.py' (making sure everything else is commented out)

4) sbatch submit.sh. Check the slurm file to make sure it ran without error and that it output the check.npy file in numpy_files folder

5) open python_scripts/step1.py. edit:

	- the os.chdir() to the working directory
	- the DATA_DIR to the trajectory directory
	- NHL_trajes to list of names of ligands in class 1 (must be same as directory names in trajectories folder)
	- same with HL
	- start, end, and skip if you want to customize the frames used. I recommed making 'end' a few frames less than the end to make sure all trajectories have equal number of frames.
	- In the for loop:
		'''
		for lig in HL_trajes:
		    for i in range(19):
		        temp=[]
		        dcd = DATA_DIR + lig + "/trajectory_prot_" + str(i) + ".xtc"
		        psf = DATA_DIR + lig + "/prot.psf"
		'''
		you will probably need to edit these lines to reflect your trajectory directory organization (and number of trajectories. NOTE: range() funtion is not inclusive of the end point!!!
	- same with NHL for loop

6) open submit.sh, comment out the check.py line and uncomment the step1.py line. then run 'sbatch submit.sh'

7) open submit.sh. comment out the step1.py line and uncomment the pairs_num.py line. run 'sbatch submit.sh'. The output file shows the total number of distance pairs, and the number of pairs per job (andes has a limit of 100 jobs)

8) open run_maker.sh. Edit the num_pairs and stride to the numbers output by the pairs_num.py (you may need to round the stride UP (not down) to the nearest integer)

9) open submit.sh. comment out the pair_num.py line and uncomment the make_CVs.py line. run './run_maker.sh'. This will submit 98 jobs.

10) open python_scripts/multi_algorithm.py. edit:
	- os.chdir() to current working directory
	- hall_ligs and nhall_ligs to list of systems to be analyzed 
	- max_nhall_prob to maximum probability of conformation in class 1 (see comments in file for details)
	- min_hall_prob to minumum probabilty of conformation in class 2 (see comments in file for details)
	- first_frame if you want to skip frames. !!!Make sure these were not skipped in the beginning!!!

11) open submit.sh. comment out the make_CV's line and uncomment the multi_algorithm.py line. run './run_maker.sh'. This will submit 98 jobs.
	- You can see if you are getting hits by checking the size of the output/ directory using 'du -hls output/' if it is more than a few dozen megabytes you probably have hits
	- If you have hits, you don't need to wait until all jobs are done, you can start analyzing with the next step. It will analyze the finished jobs

12) Go to https://jupyter.olcf.ornl.gov/

13) Sign in. navigate to working directory. open Multi_post_analysis.ipynb and/or ranking.ipynb to analyze output 
