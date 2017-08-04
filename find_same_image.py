#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'Liantian'
# __email__ = "liantian.me+code@gmail.com"
#
# Copyright 2015-2016 liantian
#
# This is free and unencumbered software released into the public domain.
# 
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
# 
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# 
# For more information, please refer to <http://unlicense.org>
import os
import pathlib
from perceptual_hash import img_hash, hamming
import random
import string


def get_image_files(work_dir=os.getcwd()):
    ext_name = ['jpg', "jpeg", 'bmp', 'png', 'gif']
    img_files = []
    for root, dirnames, fns in os.walk(work_dir):
        img_files.extend(os.path.join(root, fn) for fn in fns if any(fn.lower().endswith(ext) for ext in ext_name))
    return img_files


if __name__ == '__main__':
    #
    pictures = []
    q_map = {}

    for img_file in get_image_files():
        fp, seq = img_hash(img_file)
        pictures.append((img_file, seq))

    for item in pictures:
        # print(item)
        for other_item in pictures:
            if other_item != item:
                v = hamming(item[1], other_item[1])
                q_map[(item[0], other_item[0])] = v
        pictures.remove(item)

    for item in q_map:
        if q_map[item] < 2:
            print("{0}  ,  {1}".format(q_map[item], item))
            file0 = pathlib.Path(item[0])
            file1 = pathlib.Path(item[1])
            file0_filename, file0_ext = os.path.splitext(file0.name)
            file0_dir = file0.parent
            try:
                file1.rename(file0_dir.joinpath("{0}_{1}{2}".format(file0_filename, ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)), file0_ext)))
            except:
                pass

    # path = 'C:\\Users\\liant\\Documents\\GitHub\\SimplePicFingerprint\\example_image\\aa949cda997024700476880b642129e2.jpeg'
    # file0 = pathlib.Path(path)
    # # # print(dir(p))
    # # print(p.name)
    # # # print(p.suffix)
    #
    # file0_filename, file0_ext = os.path.splitext(file0.name)
    # file0_dir = file0.parent
    # print(file0_filename)
    # print(file0_ext)
    # print(file0_dir)
    # print()
