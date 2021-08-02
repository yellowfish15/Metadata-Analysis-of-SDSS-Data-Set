import os
import h5py
import numpy as np
from fits2hdf.io.fitsio import read_fits
from fits2hdf.io.hdfio import export_hdf


# counts the total frequency of each type among all files in all directories
sum_depth = 0 # gets the sum of all depths among all files
count_total_files = 0
count_total_directories = 0
total_attr_dtype_freq = {} # attribute types
total_dset_dtype_freq = {} # dataset types
total_unique_attr_names = {} # unique attribute names
unique_attr_datatype = {} # datatype of each unique attribute

def analyze_file_recur(f, rel_path, count_attr_dtype_freq, count_dset_dtype_freq, count_unique_attr_names):
    depth = 0
    for key in f[rel_path].keys(): # all content under this group
        item = f[rel_path][key]
        # process each attribute in this data_object
        for attr_key in item.attrs.keys(): 
            # attribute unique names
            if attr_key in count_unique_attr_names:
                count_unique_attr_names[attr_key] += 1
            else:
                count_unique_attr_names[attr_key] = 1
            if attr_key in total_unique_attr_names:
                total_unique_attr_names[attr_key] += 1
            else:
                total_unique_attr_names[attr_key] = 1

            attr_dtype = str(type(item.attrs[attr_key]))
            if isinstance(item.attrs[attr_key], np.ndarray):
                attr_dtype = str(item.attrs[attr_key].dtype)
            # attribute datatype frequencies
            if attr_dtype in count_attr_dtype_freq:
                count_attr_dtype_freq[attr_dtype] += 1
            else:
                count_attr_dtype_freq[attr_dtype] = 1
            if attr_dtype in total_attr_dtype_freq:
                total_attr_dtype_freq[attr_dtype] += 1
            else:
                total_attr_dtype_freq[attr_dtype] = 1
            unique_attr_datatype[attr_key] = str(attr_dtype)

        if isinstance(f[rel_path][key], h5py.Group): # if this object is a group
            depth = max(depth, analyze_file_recur(f, rel_path+"/"+key, count_attr_dtype_freq, count_dset_dtype_freq, count_unique_attr_names))
        else: # this object is a dataset
            dset_dtype = str(item.dtype)
            # dataset datatype frequencies
            if dset_dtype in count_dset_dtype_freq:
                count_dset_dtype_freq[dset_dtype] += 1
            else:
                count_dset_dtype_freq[dset_dtype] = 1
            if dset_dtype in total_dset_dtype_freq:
                total_dset_dtype_freq[dset_dtype] += 1
            else:
                total_dset_dtype_freq[dset_dtype] = 1
    return depth+1


# perform analysis on all ".fits" files in directory "curr_dir"
def analyze_dir(curr_dir):
    global sum_depth, count_total_files
    os.chdir(os.path.join(os.getcwd(), curr_dir))
    print("\t-- DIRECTORY ADDRESS: --\n\t" + os.getcwd() + "\n")
    '''
    Read all files ending with ".fits" extension in the current
    directory and export them to ".h5" files in the same directory
    with the same filename
    '''
    for file_ in os.listdir(os.getcwd()):
        if file_.endswith(".fits"):
            try:
                temp_file = read_fits(file_) # read in the .fits file
                export_hdf(temp_file, file_[:-5]+".h5") # export as a .h5 file
            except Exception as e:
                print(e)

    '''
    Process all files in current directory (same as this file)
    ending with file extension ".h5"
    '''
    for file_ in os.listdir(os.getcwd()):
        if file_.endswith(".h5"):
            try:
                # counts the frequency of each type in this file
                count_attr_dtype_freq = {} # attribute types
                count_dset_dtype_freq = {} # dataset types
                count_unique_attr_names = {} # unique attribute names

                print("\t" + str(file_)) # print hdf5 filename
                f = h5py.File(file_, 'r')
                file_depth = analyze_file_recur(f, '.', count_attr_dtype_freq, count_dset_dtype_freq, count_unique_attr_names)
                print("Group Structure Depth:", file_depth)
                print("Attribute Frequencies:", count_attr_dtype_freq)
                print("Dataset Frequencies:", count_dset_dtype_freq)
                print("Unique Attribute Names:", count_unique_attr_names)
                sum_depth += file_depth
                count_total_files+=1
            except OSError as e:
                print(e)


# traverse through the current directory and subdirectories
def traverse_dir_recur(curr_dir_rel):
    global count_total_directories
    print()
    analyze_dir(curr_dir_rel)
    path_abs = os.getcwd()
    directory_contents = os.listdir(path_abs)
    for item in directory_contents: # each item is a file/folder in the current directory
        if os.path.isdir(item): # if this item is a subdirectory
            traverse_dir_recur(item) # recurse on the subdirectory
            os.chdir(path_abs) # switch back to current directory when done traversing
    count_total_directories += 1

traverse_dir_recur("")

# prints total counts of each attribute type
count_total_directories-=1 # don't count current directory
print("\n\t-- TOTAL STATISTICS: --")
print("# of .fits files processed:", count_total_files)
print("# of directories processed:", count_total_directories)
if count_total_files > 0:
    print("Average File Depth:", (sum_depth/count_total_files))
print("Total Attribute Frequencies:", total_attr_dtype_freq)
print("Total Dataset Frequencies:", total_dset_dtype_freq)
print("Total Unique Attribute Names:", total_unique_attr_names)
print("Datatype of each Unique Attribute:", unique_attr_datatype)
