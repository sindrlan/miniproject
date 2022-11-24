# Importing Image class from PIL module
from PIL import Image
import os
import random
import shutil

folder = "data_norway_japan"

path = folder + "/annontations/"
dir_list = os.listdir(path)

dir_list.sort()
random.seed(230)
random.shuffle(dir_list)

split = int(0.75 * len(dir_list))

train = dir_list[:split]
val = dir_list[split:]

os.makedirs(folder + '/train/images')
os.makedirs(folder + '/val/images')
os.makedirs(folder + '/train/labels')
os.makedirs(folder + '/val/labels')

for names in val:
    shutil.copyfile(folder + "/annontations/" + names, folder + "/val/labels/" + names)
    x = names.split(".", 1)[0]
    imagepath = "/cluster/projects/vc/courses/TDT17/2022/open/RDD2022/Norway/train/images/" + x + ".jpg"
    im = Image.open(imagepath)

    width, height = im.size
    im1 = im.crop((0, 0, 2044, height))
    im1.save(folder + "/val/images/" + x + ".jpg")

for names in train:
    shutil.copyfile(folder + "/annontations/" + names, folder + "/train/labels/" + names)
    x = names.split(".", 1)[0]
    imagepath = "/cluster/projects/vc/courses/TDT17/2022/open/RDD2022/Norway/train/images/" + x + ".jpg"

    im = Image.open(imagepath)

    width, height = im.size
    im1 = im.crop((0, 0, 2044, height))
    im1.save(folder + "/train/images/" + x + ".jpg")