import os
import scipy.io as sio
import h5py
import numpy as np

def load_files(pt,data_dir='./',time_fname='linkedTimeInt.mat',anat_fname='anatInfo.mat',data_fname='linkedDataInt.mat'):
    # Import MAT files
    anat_file_path = os.path.join(data_dir,pt,anat_fname)
    anat_mat = sio.loadmat(anat_file_path)
    
    time_file_path = os.path.join(data_dir,pt,time_fname)
    time_mat = sio.loadmat(time_file_path)
    linkedTime = time_mat['linkedTime'][0]
    
    data_file_path = os.path.join(data_dir,pt,data_fname)
    with h5py.File(data_file_path, 'r') as f:
        linkedBG = np.array(f['linkedData']['linkedBG']).T
        linkedTF = np.array(f['linkedData']['linkedTF'])

    return (anat_mat,linkedTime,linkedBG,linkedTF)