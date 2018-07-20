import cv2
import numpy as np 
from sklearn.cluster import KMeans
import os
import sys

ORINGIN_TRAIN = 6471


def augment(img_path,txt_path,name,offset,n_clusters=1,one_of_fraction=4):
    ori_img = cv2.imread(os.path.join(img_path,name+'.jpg'))
    h,w = ori_img.shape[0],ori_img.shape[1]
    assert w>=h,'image width is smaller than its height!'
    gt_file = os.path.join(txt_path,name+'.txt')
    coords = []
    dets = []
    with open(gt_file,'r') as f:
        for line in f:
            l = line.strip().split(',')
            #if l[5] == '0':
            #    continue
            l = np.array(l,dtype=np.float32)
            coords.append([l[0]+0.5*l[2],l[1]+0.5*l[3]])
            dets.append(l)
    dets = np.array(dets,dtype=np.float32)
    coords = np.array(coords,dtype=np.float32)
    if len(coords)<n_clusters:
        n_clusters = len(coords)
    centers = KMeans(n_clusters=n_clusters,n_jobs=1).fit(coords).cluster_centers_
    for i,center in enumerate(centers):
        if i == 1:
            offset += ORINGIN_TRAIN
        x_min = max(0,center[0]-w/one_of_fraction)
        x_max = min(center[0]+w/one_of_fraction,w)
        if x_min == 0:
            x_max = 2*w/one_of_fraction
        if x_max == w:
            x_min = w*(1-2/one_of_fraction)
        y_min = max(0,center[1]-h/one_of_fraction)
        y_max = min(center[1]+h/one_of_fraction,h)
        if y_min == 0:
            y_max = 2*h/one_of_fraction
        if y_max == h:
            y_min = h*(1-2/one_of_fraction)
        x_min = int(x_min)
        x_max = int(x_max)
        y_min = int(y_min)
        y_max = int(y_max)
        img = ori_img[y_min:y_max+1,x_min:x_max+1,:]
        aug_img = os.path.join(img_path,'{:0>6}'.format(ORINGIN_TRAIN+offset)+'.jpg')
        cv2.imwrite(aug_img,img)

        aug_gt = os.path.join(txt_path,'{:0>6}'.format(ORINGIN_TRAIN+offset)+'.txt')
        with open(aug_gt,'wt') as f:
            for det in dets:
                print
                bbox = det[0],det[1],det[0]+det[2],det[1]+det[3]
                if bbox[2]<x_min or bbox[0]>x_max or bbox[1]>y_max or bbox[3]<y_min:
                    continue
                if bbox[0]<x_min:
                    if bbox[2]-x_min<=det[2]/2:
                        continue
                    else:
                        det[0] = x_min
                        det[2] -= x_min-bbox[0]
                if bbox[2]>x_max:
                    if x_max - bbox[0]<=det[2]/2:
                        continue
                    else:
                        det[2] = x_max-det[0]
                if bbox[1]<y_min:
                    if bbox[3]-y_min<=det[3]/2:
                        continue
                    else:
                        det[1] = y_min
                        det[3] -= y_min-bbox[1]
                if bbox[3]>y_max:
                    if y_max-bbox[1]<=det[3]/2:
                        continue
                    else:
                        det[3] = y_max-det[1]
                f.write('{:d},{:d},{:d},{:d},{:d},{:d},{:d},{:d}\n'.
                            format(int(det[0]-x_min),int(det[1]-y_min),int(det[2]),int(det[3]),int(det[4]),int(det[5]),int(det[6]),int(det[7])))

#augment('./images/','./annotations/','004504',4504)
#augment('./images/','./annotations/','000134',134,2)

def specific_augment(img_path,txt_path,name,offset,cls,n_clusters=1,one_of_fraction=4):
    ori_img = cv2.imread(os.path.join(img_path,name+'.jpg'))
    h,w = ori_img.shape[0],ori_img.shape[1]
    assert w>=h,'image width is smaller than its height!'
    gt_file = os.path.join(txt_path,name+'.txt')
    coords = []
    dets = []
    with open(gt_file,'r') as f:
        for line in f:
            l = line.strip().split(',')
            #if l[5] == '0':
            #    continue

            l = np.array(l,dtype=np.float32)
            if l[5] in cls:
                coords.append([l[0]+0.5*l[2],l[1]+0.5*l[3]])
            dets.append(l)
    dets = np.array(dets,dtype=np.float32)
    coords = np.array(coords,dtype=np.float32)
    if len(coords) == 0:
        return
    elif len(coords)<n_clusters:
        n_clusters = len(coords)

    centers = KMeans(n_clusters=n_clusters,n_jobs=1).fit(coords).cluster_centers_
    print centers
    for i,center in enumerate(centers):
        if i == 1:
            offset += 1
        x_min = max(0,center[0]-w/one_of_fraction)
        x_max = min(center[0]+w/one_of_fraction,w)
        if x_min == 0:
            x_max = 2*w/one_of_fraction
        if x_max == w:
            x_min = w*(1-2/one_of_fraction)
        y_min = max(0,center[1]-h/one_of_fraction)
        y_max = min(center[1]+h/one_of_fraction,h)
        if y_min == 0:
            y_max = 2*h/one_of_fraction
        if y_max == h:
            y_min = h*(1-2/one_of_fraction)
        x_min = int(x_min)
        x_max = int(x_max)
        y_min = int(y_min)
        y_max = int(y_max)
        img = ori_img[y_min:y_max+1,x_min:x_max+1,:]

        aug_gt = os.path.join(txt_path,'{:0>6}'.format(offset)+'.txt')
        with open(aug_gt,'wt') as f:
            for det in dets:
                bbox = det[0],det[1],det[0]+det[2],det[1]+det[3]
                if bbox[2]<x_min or bbox[0]>x_max or bbox[1]>y_max or bbox[3]<y_min:
                    continue
                if bbox[0]<x_min:
                    if bbox[2]-x_min<=det[2]/2:
                        continue
                    else:
                        det[0] = x_min
                        det[2] -= x_min-bbox[0]
                if bbox[2]>x_max:
                    if x_max - bbox[0]<=det[2]/2:
                        continue
                    else:
                        det[2] = x_max-det[0]
                if bbox[1]<y_min:
                    if bbox[3]-y_min<=det[3]/2:
                        continue
                    else:
                        det[1] = y_min
                        det[3] -= y_min-bbox[1]
                if bbox[3]>y_max:
                    if y_max-bbox[1]<=det[3]/2:
                        continue
                    else:
                        det[3] = y_max-det[1]
                f.write('{:d},{:d},{:d},{:d},{:d},{:d},{:d},{:d}\n'.
                            format(int(det[0]-x_min),int(det[1]-y_min),int(det[2]),int(det[3]),int(det[4]),int(det[5]),int(det[6]),int(det[7])))
        with open(aug_gt,'r') as f:
            notEmpty = f.readline()
        if not notEmpty:
            return
        aug_img = os.path.join(img_path,'{:0>6}'.format(offset)+'.jpg')
        cv2.imwrite(aug_img,img)


def dataset_augment(img_path,txt_path,dataset_size):
    for i in range(dataset_size):
        print(i)
        name = '{:0>6}'.format(i)
        augment(img_path,txt_path,name,i,n_clusters=2)
    print('augmentation done!')

def dataset_specific_augment(img_path,txt_path,dataset_size,offset,cls,one_of_fraction=8):
    for i in range(dataset_size):
        print(i)
        name = '{:0>6}'.format(i)
        specific_augment(img_path,txt_path,name,i+offset,cls,n_clusters=2,one_of_fraction=6)
        break
    print('augmentation done!')
#dataset_augment('./images/','./annotations/',ORINGIN_TRAIN)

dataset_specific_augment('./images/','./annotations/',ORINGIN_TRAIN,ORINGIN_TRAIN,cls=[0,1,2,3,4,5,6,7,8,9,10,11],one_of_fraction = 8)
#dataset_specific_augment('./images/','./annotations/',ORINGIN_TRAIN,ORINGIN_TRAIN*4,[1,2],8)
#dataset_specific_augment('./images/','./annotations/',ORINGIN_TRAIN,ORINGIN_TRAIN*6,[7,8],6)


