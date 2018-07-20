import os
import sys

def get_file_name(file_dir):   
    L=[]   
    for root, dirs, files in os.walk(file_dir):  
        for file in files:  
            if os.path.splitext(file)[1] == '.jpg':  
                L.append(os.path.splitext(file)[0])  
    return L 

files = get_file_name('./images/')

def rename(img_path,gt_path,files):
#def rename(img_path,files):
    for i in range(len(files)):
        img = os.path.join(img_path,files[i]+'.jpg')
        gt = os.path.join(gt_path,files[i]+'.txt')
        new_id = '{:0>6}'.format(i)
        new_img = os.path.join(img_path,new_id+'.jpg')
        new_gt = os.path.join(gt_path,new_id+'.txt')
        try:
            os.rename(img,new_img)
            os.rename(gt,new_gt)
        finally:
            pass

img_path = './images/'
gt_path = './annotations/'
rename(img_path,gt_path,files)
#rename(img_path,files)

