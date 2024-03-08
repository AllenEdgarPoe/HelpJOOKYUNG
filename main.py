path = r'C:\Users\chsjk\PycharmProjects\kohya_ss\train_dataset\hyerim_sketch_train\model\sample'
from PIL import Image
import glob
import os
import matplotlib.pyplot as plt
import time
import numpy as np
import cv2
files = glob.glob(os.path.join(path, '*.png'))
global img
image = cv2.imread(r'C:\Users\chsjk\PycharmProjects\kohya_ss\train_dataset\hyerim_sketch_train\model\sample\hyerimsketchxx_093000_00_20240228132341.png')
cv2.imshow('image window', image)
for file in files:
    cv2.destroyAllWindows()
    img = cv2.imread(file)
    cv2.imshow('window', img)
    time.sleep(3)