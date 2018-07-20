import numpy as np 
import matplotlib
import matplotlib.pyplot as plt 
import matplotlib.patches as patches
import cv2
import os

class_name = {0:'ignored regions',
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

def plot_bbox(img,dets):

    if not isinstance(dets,np.ndarray):
        dets = dets.numpy()
    
    indx = range(len(dets))
    #indx = np.where(dets[:, 5] >= 1)[0]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(img, aspect='equal')
    for i in indx:
        bbox = dets[i,:4]
        score = dets[i, 4]
        cls = class_name[dets[i,5]]
        ax.add_patch(
            patches.Rectangle((bbox[0],bbox[1]),
                               bbox[2],
                               bbox[3],fill = False,
                               edgecolor = 'green',
                               linewidth = 1.5)
            )

        ax.text(bbox[0], bbox[1] - 2,
                '{:s} {:.3f}'.format(cls, score),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=12, color='white')


    plt.axis('off')
    plt.tight_layout()
    plt.show()

def get_file_name(file_dir):
    L=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.txt':
                L.append(os.path.splitext(file)[0])
    return L

if __name__ == '__main__':
    file = get_file_name('./drow_box/txt/')
    for name in file:
        img_path = ('./drow_box/img/')
        img = cv2.imread(os.path.join(img_path,name+'.jpg'))
        gt_file = os.path.join('./drow_box/txt/',name+'.txt')
        dets = []
        with open(gt_file,'r') as f:
            for line in f:
                l = line.strip().split(',')
                l = np.array(l)
                dets.append(l)
        dets = np.array(dets,dtype=np.float32)
        plot_bbox(img,dets)