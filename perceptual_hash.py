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
#
#
# 方法参考
# http://www.ruanyifeng.com/blog/2011/07/principle_of_similar_image_search.html

import os
from PIL import Image


def img_hash(img_file, deviation=8):
    """
    :param img_file: 输入的图像路径，支持png,jpg,gif,bmp
    :param deviation: 误差值，默认是8
    :return: fp,seq 分别是指纹的字符串和序列格式

    第一步，缩小尺寸。
    将图片缩小到8x8的尺寸，总共64个像素。这一步的作用是去除图片的细节，只保留结构、明暗等基本信息，摒弃不同尺寸、比例带来的图片差异。

    第二步，简化色彩。
    将缩小后的图片，转为64级灰度。也就是说，所有像素点总共只有64种颜色。
    第三步，计算平均值。
    计算所有64个像素的灰度平均值。
    第四步，比较像素的灰度。
    将每个像素的灰度，与平均值进行比较。大于或等于平均值，记为1；小于平均值，记为0。
    第五步，计算哈希值。
    将上一步的比较结果，组合在一起，就构成了一个64位的整数，这就是这张图片的指纹。组合的次序并不重要，只要保证所有图片都采用同样次序就行了。

    """

    image = Image.open(img_file)
    # print(image.format, image.size, image.mode)
    image = image.resize((deviation, deviation), Image.ANTIALIAS)
    # image.save("step1.jpg", "JPEG")
    image = image.convert(mode="L", colors=64)
    # image.save("step2.jpg", "JPEG")
    color_seq = list(image.getdata())
    # print(color_seq)
    color_avg = sum(color_seq) / len(color_seq)
    # print(color_avg)
    result_seq = list(map(lambda x: 0 if x < color_avg else 1, [y for y in color_seq]))
    # print(result_seq)
    result_fp = format(int("".join(str(x) for x in result_seq), base=2), "x")
    return result_fp, result_seq


def hamming(s1, s2):
    """得到指纹以后，就可以对比不同的图片，看看64位中有多少位是不一样的。在理论上，这等同于计算"汉明距离"（Hamming distance）。
    如果不相同的数据位不超过5，就说明两张图片很相似；如果大于10，就说明这是两张不同的图片。"""
    assert len(s1) == len(s2)
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))
