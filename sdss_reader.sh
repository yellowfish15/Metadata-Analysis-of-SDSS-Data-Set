#!/bin/bash
#SBATCH --job-name=Read_HDF5_Files_Python
#SBATCH --output=%x.o%j
#SBATCH --error=%x.e%j
#SBATCH --partition quanah
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH --time=15:00:00
##SBATCH --mem-per-cpu=3994MB  ##3.9GB, Modify based on needs   

. $HOME/conda/etc/profile.d/conda.sh
conda activate

conda install numpy
conda install h5py

python sdss_reader.py