import numpy as np

print('num_pairs:', len(np.load('numpy_files/pairs.npy')))
print('stride:', len(np.load('numpy_files/pairs.npy'))/98)
print('stride:', np.ceil(len(np.load('numpy_files/pairs.npy'))/98))

