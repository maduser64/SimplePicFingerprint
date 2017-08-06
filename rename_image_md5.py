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
import hashlib
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

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def sha1(fname):
    hash_sha1 = hashlib.sha1()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()

if __name__ == '__main__':

    for img_file in get_image_files():
        file = pathlib.Path(img_file)
        file_filename, file_ext = os.path.splitext(file.name)
        file_dir = file.parent
        hash = sha1(img_file).upper()
        try:
            file.rename(str(file_dir.joinpath("{0}{1}".format(hash,  file_ext))))
        except:
            print(file)
            print(hash)
