#!/bin/bash
#SBATCH --job-name=Download_FITS_Data
#SBATCH --output=%x.o%j
#SBATCH --error=%x.e%j
#SBATCH --partition nocona
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --time=10:00:00
##SBATCH --mem-per-cpu=3994MB  ##3.9GB, Modify based on needs

. $HOME/conda/etc/profile.d/conda.sh
conda activate

conda install BeautifulSoup4
conda install lxml
conda install requests

python wget_download_auto.py

