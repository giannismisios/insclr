'''Reads the partof_train_clean.csv and for each image name searches its url from the train.csv
 and downloads it to a specific folder based on its name'''

import os
import pandas as pd
import numpy as np
import wget
from image_downloader import download_image

root = 'download/datasets/gldv2'
input1 = 'partof_train_clean.csv' # download from https://s3.amazonaws.com/google-landmark/metadata/train_clean.csv
input2 = 'train.csv'  # download from https://s3.amazonaws.com/google-landmark/metadata/train.csv

def download_file(root, image,  image_url):
    local_path = os.path.join(root, image[0], image[1], image[2])
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    local_path = os.path.join(local_path,image + ".jpg")
    if not os.path.exists(local_path):
        wget.download(image_url[0], local_path)

train = pd.read_csv(os.path.join(root, input2))

with open(os.path.join(root, input1), "r") as fr:
    lines = (line.strip() for line in fr.readlines())

    for idx, line in enumerate(lines):
        # specify the number of classes to download their correspondence images
        if idx == 20:
            exit()
        if idx == 0:
            # skip the first line
            continue

        landmark, imgs = line.split(",")
        landmark = int(landmark)
        split_imgs = imgs.split()

        for image in split_imgs:
            row = np.where(train['id']==str(image))
            image_url = train['url'].values[row]
            local_path = os.path.join(root, image[0], image[1], image[2])

            # check about path existence
            if not os.path.exists(local_path):
                os.makedirs(local_path)
            local_path = os.path.join(local_path,image + ".jpg")
            # check about image duplicates
            if not os.path.exists(local_path):
                download_image(image_url[0], local_path)
