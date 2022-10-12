# -*- coding: utf-8 -*-
"""prepeocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LxM0ccImVP_YxmZSdbA_1laASQ5ZiFkz
"""

import os
import numpy as np
import pywt
import cv2
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tqdm import tqdm
from pylab import *
from pywt._doc_utils import wavedec2_keys, draw_2d_wp_basis
import scipy
from skimage import filters
from skimage.color import rgb2lab
from skimage.morphology import square,opening,closing,dilation,erosion,skeletonize
from PIL import Image, ImageFilter,ImageOps
from pandas import *
import os
from os import listdir

from google.colab import drive
drive.mount('/content/drive')

#for j in tqdm(os.listdir(rootDir)):
  #img=mpimg.imread(os.path.join(rootDir,j))
#img=mpimg.imread("/content/img.png")
gray_1=mpimg.imread("/content/drive/MyDrive/DSPSD_Project/Malignant-1.png")
plt.imshow(gray_1, cmap='gray')
plt.axis('off')
plt.title("Grayscale image")

fix_img = cv2.cvtColor(gray_1, cv2.COLOR_BGR2RGB)
R, G, B = fix_img[:,:,0], fix_img[:,:,1],fix_img[:,:,2]

print(R.shape,G.shape,B.shape,R.max(),G.max(),B.max())

print(fix_img.shape)

for i in range(3):
  res=fix_img[:,:,i]
  if(res.mean()<1):
    res=(res*255)
    res=floor(res)
    res=res.astype(uint8)
    fix_img[:,:,i]=res

print(R.shape,G.shape,B.shape,R.max(),G.max(),B.max())

Y=G
Z=opening(Y,square(3))

plt.imshow(Z,cmap='gray')
plt.axis('off')
plt.title("Green Channel")

print(Z.shape,Z.max())

# clahe = cv2.createCLAHE(clipLimit=6)
# equalized = clahe.apply(gray_1)
# plt.imshow(equalized,cmap='gray')
# plt.axis('off')
# plt.title("CLAHE on gray")

Z=Z.astype(uint8)

clahe1 = cv2.createCLAHE(clipLimit =6)
enhanced = clahe1.apply(Z)
plt.imshow(enhanced,cmap='gray')
plt.axis('off')
plt.title("CLAHE on Green" )

imageinv = cv2.bitwise_not(enhanced)
plt.imshow(imageinv,cmap='gray')
plt.axis('off')
plt.title("Inverse of CLAHE")

imageinvnew1=opening(imageinv,square(11))
plt.imshow(imageinvnew1,cmap='gray')
plt.axis('off')

imgsub = cv2.subtract(imageinv,imageinvnew1)

plt.imshow(imgsub,cmap='gray')
plt.axis('off')

(thresh, im_bw) = cv2.threshold(imgsub, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
print(thresh)

plt.imshow(im_bw ,cmap='gray')
plt.axis('off')

nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(im_bw, None, None, None, 8, cv2.CV_32S)

areas = stats[1:,cv2.CC_STAT_AREA]

result = np.zeros((labels.shape), np.uint8)

for i in range(0, nlabels - 1):
    if areas[i] >= 100:   #keep
        result[labels == i + 1] = 255

plt.imshow(result,cmap='gray')
plt.axis('off')

plt.imshow(enhanced,cmap='gray')
plt.axis('off')

imageinvnew=closing(enhanced,square(11))
plt.imshow(imageinvnew,cmap='gray')
plt.axis('off')

(opticthresh, optic_bw) = cv2.threshold(enhanced, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
print(opticthresh)
plt.imshow(optic_bw,cmap='gray')
plt.axis('off')

x1=closing(optic_bw,square(4))
plt.imshow(x1,cmap='gray')
plt.axis('off')

x1= cv2.bitwise_not(x1)
plt.imshow(x1,cmap='gray')
plt.axis('off')

x4= cv2.subtract(x1,result)
plt.imshow(x4,cmap='gray')
plt.axis('off')

nlabels, labels, stats, jicentroids = cv2.connectedComponentsWithStats(x4, None, None, None, 8, cv2.CV_32S)