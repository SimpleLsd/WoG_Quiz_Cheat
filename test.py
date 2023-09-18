# import Levenshtein

# given_string = "Browning M2"

# # 六个候选字符串
# candidate_strings = ["BAR", "Browning M2", "DShK",
#                      "Hotchkiss M1909", "Ultimax 100", "RPD"]

# # 初始化最小距离和最接近的字符串索引
# min_distance = float('inf')
# closest_index = None

# # 遍历候选字符串并计算Levenshtein距离
# for index, candidate in enumerate(candidate_strings):
#     distance = Levenshtein.distance(given_string, candidate)
#     if distance < min_distance:
#         min_distance = distance
#         closest_index = index

# print(closest_index)
# screenshot_test = ImageGrab.grab(bbox=r_1).convert('RGB')
import pyautogui
from PIL import ImageGrab

import mss

r_1 = (100, 100, 300, 300)

with mss.mss() as sct:
    region = {'top': 0, 'left': 0, 'width': 400, 'height': 300}
    # 指定捕获区域的坐标和大小，同时指定保存路径
    img = sct.grab(region)
    mss.tools.to_png(img.rgb, img.size, output='dummy.png')
    img.save('test.png')
