# coding: utf-8

import os
import random
import shutil

rootdir = "/home/momenta/MC_data/images_12k/"
file_names = []
for parent, dirnames, filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    file_names = filenames
    # for filename in filenames:                        #输出文件信息
    #     print("parent is" + parent)
    #     print("filename is:" + filename)
    #     print("the full name of the file is:" + os.path.join(parent, filename))
L =[]
for i in range(2000):
    x = random.randint(0, len(file_names)-1)

    if x in L:
        continue
    L.append(x)
    shutil.copyfile( rootdir + file_names[x], "/home/momenta/MC_data/images/" + file_names[x])
    os.remove(rootdir + file_names[x])
    jsonname = file_names[x] + ".json"
    shutil.copyfile( '/home/momenta/MC_data/labels_12k/' + jsonname, "/home/momenta/MC_data/annotation/" + jsonname)
    os.remove('/home/momenta/MC_data/labels_12k/' + jsonname)
    print(file_names[x])
    print i