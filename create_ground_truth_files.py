import argparse
import numpy as np
import os
import pandas as pd

from os.path import join, exists, isfile
from patchnetvlad.tools import PATCHNETVLAD_ROOT_DIR

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Patch-NetVLAD-Ground-Truth-Files-Create')

    parser.add_argument('--data_type', type=str, default='mapillarysf', required=True, choices=['mapillarysf'])
    parser.add_argument('--raw_dataset_file_dir', type=str, required=True)
    parser.add_argument('--output_gt_dir', type=str, required=True)

    opt = parser.parse_args()

    print(opt)

    if opt.data_type == 'mapillarysf':
        image_files_list = [
            join(PATCHNETVLAD_ROOT_DIR, 'dataset_imagenames', opt.data_type + '_imageNames_query.txt'),
            join(PATCHNETVLAD_ROOT_DIR, 'dataset_imagenames', opt.data_type + '_imageNames_index.txt')
        ]

        utmQ = utmDb = None
        for i, file_path in enumerate(image_files_list):
            with open(file_path, 'r') as f:
                image_list = f.read().splitlines()

            # 读取图片列表
            image_name_list = [(os.path.split(image)[1]).split('.')[0] for image in image_list]

            utm_type = ((os.path.split(file_path)[1]).split('.')[0]).split('_')[-1]

            if utm_type == 'query':
                utm_file = join(opt.raw_dataset_file_dir, 'query', 'postprocessed.csv')
            else:
                utm_file = join(opt.raw_dataset_file_dir, 'database', 'postprocessed.csv')

            db_data = pd.read_csv(utm_file)

            if utm_type == 'query':
                utmQ = np.array([(db_data[db_data['key'] == image_name])[['easting', 'northing']].values.squeeze()
                                 for image_name in image_name_list])
            else:
                utmDb = np.array([(db_data[db_data['key'] == image_name])[['easting', 'northing']].values.squeeze()
                                  for image_name in image_name_list])

        np.savez(join(opt.output_gt_dir, opt.data_type + '.npz'), utmQ=utmQ, utmDb=utmDb, posDistThr=25)

    print('Creat {} Ground Truth Files Done!!!'.format(opt.data_type))
