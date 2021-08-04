import torch
import torchvision.models as models
import numpy as np
import random
import h5py

from os.path import join

if __name__ == '__main__':
    initcache = join('patchnetvlad/desired/cache/mapillary',
                     'centroids', 'vgg16_' + 'mapillary_16' + '_desc_cen.hdf5')

    with h5py.File(initcache, mode='r+') as h5:
        print('11111111111111111')

    with h5py.File(initcache, mode='r+') as h6:
        print('2222222222')


    print('xxx')
