#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import imageio
import skimage
from multiprocessing import Pool

# images_path = '/home/abtin/projects/def-najjaran/abtin/Data/DLR/Data/Virtual_Simulation/Images/'
annotations_path = os.path.join(os.environ['SLURM_TMPDIR'],'work/Data/Virtual_Simulation/Annotations/')
masks_path = os.path.join(os.environ['SLURM_TMPDIR'], 'work/Data/Virtual_Simulation/Masks/')
annotations = [f for f in os.listdir(annotations_path) if f.endswith(".png")]

# type = 'real'
type = 'virtual'

brkn = open("broken.txt","w")

def masking(name):
    try:
        im = np.array(imageio.imread(os.path.join(annotations_path + name)))
        new_im = im.reshape((im.shape[0]*im.shape[1]), im.shape[2])
        mask = np.zeros([np.shape(im)[0], np.shape(im)[1]])
        
        for x in range(np.shape(im)[0]):
            for y in range(np.shape(im)[1]):
                if not np.all(im[x,y][:3] == im[x,y][0]):
                    
                    if type == 'real':
                        if np.max(im[x,y][:3]) == im[x,y][0]: # fabric - red
                            mask[x,y] = 50
                        elif np.max(im[x,y][:3]) == im[x,y][1]: # wrinkle - green
                            mask[x,y] = 100

                    if type == 'virtual':
                        if np.max(im[x, y][:3]) == im[x, y][0]:  # wrinkle - red
                            mask[x, y] = 100
                        elif np.max(im[x, y][:3]) == im[x, y][1]:  # fabric - green
                            mask[x, y] = 50

                    if np.max(im[x,y][:3]) == im[x,y][2]: # gripper - blue
                        mask[x,y] = 200

        mask = mask.astype(int)*255
        imageio.imwrite('{}{}.png'.format(masks_path, name[:-4]), mask.astype(np.uint8))

        print("{} converted to masks".format(name))

    except IndexError:

        brkn.write(name + "\n")
        pass

if __name__ == '__main__':
    pool = Pool(os.cpu_count()-2)
    pool.map(masking, annotations)
