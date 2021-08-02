# Metadata Analysis of SDSS Datasets
Python scripts to analyze FITS files from the Sloan Digital Sky Survey
Note: this study was conducted in a Linux Operating System Environment

## Retrieving Data from the SDSS Database
To download files from a portion of the SDSS Database, use the wget_download_auto.py script
Note: If you are using another operating system such as MacOS or Windows, you may need to install the wget command before using this script
Note: This script will recursively download all FITS files in the specified url directory and all subdirectories
Note: A shell executable script is provided in case you wish to submit this as a job query to an HPC Cluster running SLURM

1. Place the script in a folder or directory where you would like to download the data to.
2. Copy the base directory url in the remote SDSS database where you want to start downloading FITS files from
3. Paste this url into the bottom of the script as the first paramater of the "url_download_recur" function (for reference some sample lines are provided in comments)
4. The lowest directory in the url is the second paramter for the function
5. Both paramters should be passed into the url_download_recur function as Strings
6. Run the script to begin the recursive downloading process

## Extracting Metadata From Downloaded FITS Files
To convert from FITS to HDF5 and extract metadata, use the sdss_reader.py script
Note: You need to first download the fits2hdf tool and follow the installation instructions at https://fits2hdf.readthedocs.io/en/latest/getting_started.html

1. Place this script in the directory where you want to convert and analyze FITS Files in HDF5 Format
2. Make sure any subdirectories you do not wish to be processed are cleared from the current directory
3. If you don't want the script to recurse down subdirectories, you can comment out lines 112 to 116
4. Run the script and the statistical results will be print out to the terminal

