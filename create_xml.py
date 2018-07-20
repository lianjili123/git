#encoding=utf-8

import sys
import os
import codecs
import cv2
import glob
import json

#src = open('/home/lianji/MC_data/train_data/example/00002150_all_videos_robot2_03_mp4.jpg.json')
#obj = json.loads(src.read())

n = 0
jsonlist=glob.glob('./train_data/labels_12k/*.json')
for json_ in jsonlist:
    jsonname = os.path.basename(json_)
    name = os.path.splitext(jsonname)[0]
    print name
    jpgpath = os.path.join('./train_data/images_12k/'+ name)
    #print jpgpath
    src = open(json_, 'r')
    obj = json.loads(src.read())
    img = cv2.imread(jpgpath)
    sp = img.shape
    #print sp
    height = sp[0]
    width = sp[1]
    depth = sp[2]
    #uavinfo = flabel.readlines()
    #fp2 = open('train.txt', 'w')
    #fp2.writelines(name + '\n')
    n = n + 1
    print n
    with codecs.open(r'./annotations/'+ name + '.xml', 'w', 'utf-8') as xml:
        xml.write('<annotation>\n')
        xml.write('\t<folder>' + 'VOC2007' + '</folder>\n')
        xml.write('\t<filename>' + name + '</filename>\n')
        xml.write('\t<source>\n')
        xml.write('\t\t<database>VisDrone</database>\n')
        xml.write('\t\t<annotation>PASCAL VOC2007</annotation>\n')
        xml.write('\t\t<image>flickr</image>\n')
        xml.write('\t\t<flickrid>NULL</flickrid>\n')
        xml.write('\t</source>\n')
        xml.write('\t<owner>\n')
        xml.write('\t\t<flickrid>NULL</flickrid>\n')
        xml.write('\t\t<name>lianji</name>\n')
        xml.write('\t</owner>\n')
        xml.write('\t<size>\n')
        xml.write('\t\t<width>'+ str(width) + '</width>\n')
        xml.write('\t\t<height>'+ str(height) + '</height>\n')
        xml.write('\t\t<depth>' + str(depth) + '</depth>\n')
        xml.write('\t</size>\n')
        xml.write('\t\t<segmented>0</segmented>\n')
        if not 'Rects' in obj:
            xml.write('</annotation>')
            continue
        for i in range(len(obj['Rects'])):
            l_pos1 = obj['Rects'][i]['x']
            l_pos2 = obj['Rects'][i]['y']
            if l_pos1 < 0:
                l_pos1 = 0
            if l_pos2 < 0:
                l_pos2 = 0
            r_pos1 = str(l_pos1 + obj['Rects'][i]['w'])
            r_pos2 = str(l_pos2 + obj['Rects'][i]['h'])
            l_pos1 = str(l_pos1)
            l_pos2 = str(l_pos2)
            print l_pos1


            classname = str(obj['Rects'][i]['properties']['world_cup'])


            xml.write('\t<object>\n')
            xml.write('\t\t\t<name>' + classname + '</name>\n')
            xml.write('\t\t<pose>Unspecified</pose>\n')
            xml.write('\t\t<truncated>0</truncated>\n')
            xml.write('\t\t<difficult>0</difficult>\n')
            xml.write('\t\t<bndbox>\n')
            xml.write('\t\t\t<xmin>' + l_pos1 + '</xmin>\n')
            xml.write('\t\t\t<ymin>' + l_pos2 + '</ymin>\n')
            xml.write('\t\t\t<xmax>' + r_pos1 + '</xmax>\n')
            xml.write('\t\t\t<ymax>' + r_pos2 + '</ymax>\n')
            xml.write('\t\t</bndbox>\n')
            xml.write('\t</object>\n')
        xml.write('</annotation>')
    src.close()
    #break
    #fp2.close()
