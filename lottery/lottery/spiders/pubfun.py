#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Author: ylf
#
# Created: 16-12-19

import os
import hashlib
from PIL import Image
from lottery.settings import DSTPATH
from os import listdir


def is_chinese(uchar):

    """判断一个unicode是否是汉字"""

    if uchar >= u'/u4e00' and uchar<= u'/u9fa5':

        return True

    else:

        return False


def splitimage(src, rownum, colnum, dstpath, fpath):
    #src 文件所在路径 rownum 行数 colnum 列数 dstpath 保存路径 name scrapy name
    img = Image.open(src)
    w, h = img.size
    if rownum <= h and colnum <= w:
        s = os.path.split(src)
        if dstpath == '':
            dstpath = s[0]
        fn = s[1].split('.')
        basename = fn[0]
        ext = fn[-1]

        num = 0
        rowheight = h // rownum
        colwidth = w // colnum
        opencode = []
        filepath = "{}/lottery/spiders/{}/".format(os.path.abspath('.'), fpath)
        filelist = listdir(filepath)
        for r in range(rownum):
            for c in range(colnum):
                box = (c * colwidth, r * rowheight, (c + 1) * colwidth, (r + 1) * rowheight)
                img.crop(box).save(os.path.join(dstpath, basename + '_' + str(num) + '.' + ext), ext)
                filename = os.path.join(dstpath, basename + '_' + str(num) + '.' + ext), ext
                #计算每个图片的md5值
                result = CalcMD5(filename[0])
                for doc in filelist:
                    if doc.startswith(result[0]):
                        opencode.append(doc.split('.')[1])
                        os.system('rm -rf {}'.format(result[1]))

                num = num + 1

        mess = '图片切割完毕，共生成 %s 张小图片。' % num
    else:
        opencode = ""
        mess = '不合法的行列切割参数！'
    return opencode


def CalcMD5(filepath):
    with open(filepath,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        os.rename(filepath, "{}/{}_{}".format(DSTPATH, hash, filepath.split('/')[-1]))
        result =  "{}/{}_{}".format(DSTPATH, hash, filepath.split('/')[-1])
        return hash,result



