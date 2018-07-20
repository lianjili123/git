#encoding=utf-8

import sys
import os
import codecs
import cv2
import glob

class_name = {
              0:'ignored regions',
              1:'pedestrian',
              2:'people',
              3:'bicycle',
              4:'car',
              5:'van',
              6:'truck',
              7:'tricycle',
              8:'awning_tricycle',
              9:'bus',
              10:'motor',
              11:'others'
            }
n = 0
textlist=glob.glob('./annotations/*.txt')
for text_ in textlist:
    txtname = os.path.basename(text_)
    name = os.path.splitext(txtname)[0]
    jpgpath = os.path.join('./images/'+ name +'.jpg')
    print jpgpath
    flabel = open(text_, 'r')
    img = cv2.imread(jpgpath)
    sp = img.shape
    #print sp
    height = sp[0]
    width = sp[1]
    depth = sp[2]
    uavinfo = flabel.readlines()
    #fp2 = open('train.txt', 'w')
    #fp2.writelines(name + '\n')
    n = n + 1
    print n
    with codecs.open(r'./VOC2007/Annotations/'+ name + '.xml', 'w', 'utf-8') as xml:
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
        for i in range(len(uavinfo)):
            line = uavinfo[i]
            line = line.strip().split(',')
            if line[0] == '0':
                l_pos1 = '1'
            else:
                l_pos1 = line[0]
            #l_pos1 = line[0]
            if line[1] == '0':
                l_pos2 = '1'
            else:
                l_pos2 = line[1]
            #l_pos2 = line[1]
            r_pos1 = int(l_pos1) + int(line[2])
            r_pos2 = int(l_pos2) + int(line[3])

            if r_pos1 == height:
                r_pos1 = str(r_pos1 - 1)
            else:
                r_pos1 = str(r_pos1)

            if r_pos2 == height:
                r_pos2 = str(r_pos2 - 1)
            else:
                r_pos2 = str(r_pos2)


            #print r_pos1
            #print r_pos2
            classname = class_name[int(line[5])]


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
    flabel.close()
    #break
    #fp2.close()
