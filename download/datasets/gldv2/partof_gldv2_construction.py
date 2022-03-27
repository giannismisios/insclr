''' Splits the 'train_clean.csv' file in a new .csv file
containing only the landmark_ids having more than 15 images and
their corresponding image names'''

import os
import csv
import pandas as pd


root = 'download/datasets/gldv2'
input = 'train_clean.csv'

with open(os.path.join(root, input), "r") as fr:
    lines = (line.strip() for line in fr.readlines())

    label = 0
    _landmark = []
    _images = []

    for idx, line in enumerate(lines):
        if idx == 0:
            # skip the first line
            continue

        landmark, imgs = line.split(",")
        landmark = int(landmark)
        split_imgs = imgs.split()

        if len(split_imgs) >= 15:
            _landmark.append(landmark)
            _images.append(imgs)

    df = pd.DataFrame(zip(_landmark,_images ), columns=['landmark_id','images'])
    df.to_csv('partof_train_clean.csv', index=False)
