import cv2
import numpy as np
import Levenshtein

pixel_coordinates = [(0, 0), (236, 157)]


# def get_img_feature(img):
#     # 将图像转换为HSV颜色空间
#     hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#     # 计算颜色直方图
#     hist_value = cv2.calcHist([hsv_img], [2], None, [50], [0, 256])

#     # 将直方图归一化
#     hist_value /= hist_value.sum()

#     # 将三个颜色通道的直方图合并成一个特征向量
#     feature_vector = np.concatenate((hist_value), axis=None)

#     # 转换 NumPy 数组为列表
#     feature_vector = [round(float(value), 8) for value in feature_vector]

#     return feature_vector


def get_gun_name_by_feature(feature_vector, guns_feature_dict):
    # 计算差异值（欧氏距离）
    # print(guns_feature_dict)
    diff = {}
    for key, value in guns_feature_dict.items():
        diff[key] = round(np.linalg.norm(
            np.array(value) - np.array(feature_vector)), 4)

    # 按差异值从小到大排序
    sorted_diff = sorted(diff.items(), key=lambda x: x[1])

    # print("差异值列表：", sorted_diff)
    # print(sorted_diff[0][1])

    if sorted_diff[0][1] < 50:
        return sorted_diff[0][0]
    else:
        return 'none'


def get_option_name_by_feature(feature_vector, options_feature_dict):
    diff = {}
    for key, value in options_feature_dict.items():
        diff[key] = round(np.linalg.norm(
            np.array(value) - np.array(feature_vector)), 4)

    # 按差异值从小到大排序
    sorted_diff = sorted(diff.items(), key=lambda x: x[1])

    # print("差异值列表：", sorted_diff)
    # print(sorted_diff[0][1])

    if sorted_diff[0][1] < 15:
        return sorted_diff[0][0]
    else:
        return 'none'


def get_gunimg_feature(img):
    # image = cv2.imread(img)
    pixel_coordinates = [(0, 0), (236, 157), (0, 80), (12, 80), (24, 80), (36, 80), (48, 80), (60, 80), (72, 80), (84, 80), (
        96, 80), (108, 80), (120, 80), (132, 80), (144, 80), (156, 80), (168, 80), (180, 80), (192, 80), (204, 80), (216, 80), (228, 80), (132, 32), (132, 44), (132, 56), (132, 68), (132, 92), (132, 104), (132, 116), (132, 128)]

    brightness_values = []
    for x, y in pixel_coordinates:
        brightness = float(img[y, x][0])
        brightness_values.append(brightness)

    # print("亮度值列表:", brightness_values)
    return brightness_values


def get_optionimg_feature(img):
    pixel_coordinates = [
        (60, 16), (66, 16), (68, 16), (72, 16), (76, 16), (80, 16),
        (84, 16), (88, 16), (92, 16), (96, 16), (100, 16), (104, 16),
        (108, 16), (112, 16), (116, 16), (120, 16), (124, 16), (128, 16),
        (132, 16), (136, 16),
        (60, 18), (66, 18), (68, 18), (72, 18), (76, 18), (80, 18),
        (84, 18), (88, 18), (92, 18), (96, 18), (100, 18), (104, 18),
        (108, 18), (112, 18), (116, 18), (120, 18), (124, 18), (128, 18),
        (132, 18), (136, 18),
        (60, 20), (66, 20), (68, 20), (72, 20), (76, 20), (80, 20),
        (84, 20), (88, 20), (92, 20), (96, 20), (100, 20), (104, 20),
        (108, 20), (112, 20), (116, 20), (120, 20), (124, 20), (128, 20),
        (132, 20), (136, 20),
        (126, 18), (126, 20), (130, 20)
    ]

    brightness_values = []
    # print(img)
    # print(img)
    for x, y in pixel_coordinates:
        brightness = float(img[y, x][0])
        brightness_values.append(brightness)

    # print("亮度值列表:", brightness_values)
    return brightness_values


def get_option_index(given_string, candidate_strings):
    # 初始化最小距离和最接近的字符串索引
    min_distance = float('inf')
    closest_index = None
    # 遍历候选字符串并计算Levenshtein距离
    for index, candidate in enumerate(candidate_strings):
        distance = Levenshtein.distance(given_string, candidate)
        if distance < min_distance:
            min_distance = distance
            closest_index = index

    print("最小距离", min_distance)
    if min_distance < 1:
        return closest_index
    else:
        return None
