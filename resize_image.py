# coding=utf-8
'''
@Author: Kyle
@Date: 2020-03-06 12:46:48
@LastEditors: Kyle
@LastEditTime: 2020-03-06 13:04:13
@Description: 
@FilePath: /my_script/resize_image.py
'''

import sys
from glob import glob
# pip install Pillow
from PIL import Image
import os
import math

THRESHOLD = 500000 
NEW_W_H = 2000


def resize_images(source_dir, target_dir, threshold, new_w_or_h):
    filenames = glob('{}/*'.format(source_dir))
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for filename in filenames:
        output_filename = filename.replace(source_dir, target_dir)
        resize_image(filename, target_path=output_filename,
                     threshold=threshold, new_w_or_h=new_w_or_h)


def resize_image(source_path, target_path, threshold, new_w_or_h):
    filename = source_path
    filesize = os.path.getsize(filename)
    if filesize >= threshold:
        print(filename)
        with Image.open(filename) as im:
            width, height = im.size
            if width >= height:
                new_width = new_w_or_h
                new_height = int(new_width * height * 1.0 / width)
            else:
                new_height = new_w_or_h
                new_width = int(new_height * width * 1.0 / height)
            resized_im = im.resize((new_width, new_height))
            resized_im.save(target_path)


# resize_images(SORUCE_DIR, TARGET_DIR, THRESHOLD, NEW_W_H)

if __name__ == "__main__":
    source_path = sys.argv[1]
    dest_path = sys.argv[2]
    if dest_path is None:
        dest_path = source_path
    resize_image(source_path, dest_path, THRESHOLD, NEW_W_H)
