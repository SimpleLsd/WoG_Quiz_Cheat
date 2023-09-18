import cv2
import os
import json

import functions as f

gun_img_folder_path = './output_folder'

guns_feature_dict = {}

for filename in os.listdir(gun_img_folder_path):
    if filename.endswith(('.jpg')):  # 仅处理图像文件，可以根据需要添加其他扩展名
        # 拼接完整的文件路径
        img_path = os.path.join(gun_img_folder_path, filename)

        # 使用OpenCV读取图像
        img = cv2.imread(img_path)

        feature_vector = f.get_gunimg_feature(img)

        guns_feature_dict[filename] = list(feature_vector)

with open('guns_feature_dict.json', 'w') as f:
    json.dump(guns_feature_dict, f)
