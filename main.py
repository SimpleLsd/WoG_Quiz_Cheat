import sys
import os
import math
import json
import cv2
import pyautogui
import numpy as np
import functions as fun
import random
import string
import time

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QColor
from functools import partial
from pytesseract import image_to_string as its
from PIL import ImageGrab


position = (192, 820)

with open('guns_feature_dict.json', 'r') as file:
    guns_feature_dict = json.load(file)

with open('options_feature_dict.json', 'r') as file:
    options_feature_dict = json.load(file)


def euclidean_distance(vector1, vector2):
    distance = math.sqrt(sum((x - y) ** 2 for x, y in zip(vector1, vector2)))
    return distance


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        self.rect_color = Qt.white  # 初始颜色为白色
        self.label_text = "等待操作"

        # 设置窗口属性
        self.setWindowTitle("作弊器")
        self.setGeometry(position[0], position[1], 400, 296)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1)

        # 创建标签
        self.label = QLabel(self)
        self.label.setText(self.label_text)
        self.label.setStyleSheet("color: white;")

        font = QFont()
        font.setBold(True)
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setGeometry(10, 264, 200, 50)

        # 创建按钮
        self.button_capture = QPushButton("GO!", self)
        self.button_capture.setGeometry(10, 220, 60, 30)
        self.button_capture.clicked.connect(self.main)

        self.button_close = QPushButton("关闭", self)
        self.button_close.setGeometry(10, 250, 60, 30)
        self.button_close.clicked.connect(self.close_window)

        self.button_close = QPushButton("测试", self)
        self.button_close.setGeometry(240, 220, 60, 30)
        self.button_close.clicked.connect(self.test)

        self.button_close = QPushButton("刷新枪械文件", self)
        self.button_close.setGeometry(310, 220, 90, 30)
        self.button_close.clicked.connect(self.register_guns_from_files)

        self.button_close = QPushButton("刷新选项文件", self)
        self.button_close.setGeometry(310, 250, 90, 30)
        self.button_close.clicked.connect(self.register_options_file)

        # self.button_close = QPushButton("注册当前选项", self)
        # self.button_close.setGeometry(320, 250, 80, 30)
        # self.button_close.clicked.connect(self.register_options_now)

        self.button_close = QPushButton("注册1", self)
        self.button_close.setGeometry(90, 220, 60, 20)
        self.button_close.clicked.connect(partial(self.register, 1))

        self.button_close = QPushButton("注册2", self)
        self.button_close.setGeometry(150, 220, 60, 20)
        self.button_close.clicked.connect(partial(self.register, 2))

        self.button_close = QPushButton("注册3", self)
        self.button_close.setGeometry(90, 240, 60, 20)
        self.button_close.clicked.connect(partial(self.register, 3))

        self.button_close = QPushButton("注册4", self)
        self.button_close.setGeometry(150, 240, 60, 20)
        self.button_close.clicked.connect(partial(self.register, 4))

        self.button_close = QPushButton("注册5", self)
        self.button_close.setGeometry(90, 260, 60, 20)
        self.button_close.clicked.connect(partial(self.register, 5))

        self.button_close = QPushButton("注册6", self)
        self.button_close.setGeometry(150, 260, 60, 20)
        self.button_close.clicked.connect(partial(self.register, 6))

        self.installEventFilter(self)

        self.drag_position = None

        self.setFocus()

    def main(self):
        print('--------------------------------------')
        time.sleep(0.2)

        gun_name = self.get_gun_name()

        if gun_name != "none":
            print(gun_name)
            self.changeLabelText(gun_name, "#05e305")

            # 从特征库识别文字
            screenshots_cv2 = self.get_options_screenshots()[1]
            option_names_f = self.get_options_names_by_features(
                screenshots_cv2)
            print('特征识别', option_names_f)

            # 遍历从特征库识别的文字，取出最接近的那个索引值
            option_index = self.get_option_index_strict(
                gun_name, option_names_f)
            # print('特征识别索引', option_index)

            # for i in range(len(option_names_f)):
            #     if option_names_f[i] == 'none':
            #         self.test(gun_name, option_names_f, screenshots_cv2)

            self.mouse_auto_click(option_index)

            if option_index != -1:
                self.main()

        else:
            self.changeLabelText("未识别", "#FF1122")

    def test(self, gun_name, option_names_f, screenshots_cv2):
        print('+++++++++++++++++++++++++++++++++++++++')

        # print("获取截图到test文件夹")
        # self.get_options_screenshots()

        print("从截图通过OCR识别文字")
        option_names_ocr = self.get_options_names_by_pytesseract(
            screenshots_cv2)
        print(option_names_ocr)

        # 遍历从特征库识别的文字，如果有空，取出索引值
        none_indices = [index for index, item in enumerate(
            option_names_f) if item == 'none']
        print("库中不存在的索引", none_indices)

        # 然后注册对应的选项
        self.get_options_register_one(
            none_indices, option_names_ocr, screenshots_cv2)

    def get_option_index_strict(self, gun_name, option_names):
        for i in range(len(option_names)):
            if option_names[i] == gun_name:
                return i

        return -1

    def get_gun_name(self):
        window_position = self.pos()
        left = window_position.x() + 90  # 左上角的 x 坐标
        top = window_position.y() + 49   # 左上角的 y 坐标
        right = window_position.x() + 237 + 90  # 右下角的 x 坐标
        bottom = window_position.y() + 49 + 158  # 右下角的 y 坐标

        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
        screenshot = screenshot.convert('RGB')
        # screenshot.save("screenshot.png")

        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        # print(screenshot)

        feature_vector = fun.get_gunimg_feature(screenshot)
        # print("本次特征", feature_vector)

        return fun.get_gun_name_by_feature(feature_vector, guns_feature_dict)

    def register_options_file(self):
        gun_img_folder_path = './options'
        guns_feature_dict = {}

        num = 0

        for filename in os.listdir(gun_img_folder_path):
            if filename.endswith(('.png')):  # 仅处理图像文件，可以根据需要添加其他扩展名
                # 拼接完整的文件路径
                img_path = os.path.join(gun_img_folder_path, filename)

                # 使用OpenCV读取图像
                img = cv2.imread(img_path)

                feature_vector = fun.get_optionimg_feature(img)

                guns_feature_dict[filename[:-4]] = list(feature_vector)

                num += 1

        with open('options_feature_dict.json', 'w') as f:
            json.dump(guns_feature_dict, f)

        print("注册完成目前有", num, "为", round(num/242*100, 2), "%")

    def register_options_now(self):
        screenshots_img, screenshots_cv2 = self.get_options_screenshots()
        option_names = self.get_options_names_by_pytesseract(screenshots_img)
        print(option_names)
        self.get_options_register(option_names, screenshots_cv2)

    def get_options_screenshots(self):
        window_position = self.pos()
        width = 199
        height = 29

        o_left = window_position.x()
        o_top = window_position.y() + 299

        o_0 = o_left, o_top, width, height
        o_1 = o_left + 201, o_top, width, height
        o_2 = o_left, o_top + 31, width, height
        o_3 = o_left + 201, o_top + 31, width, height
        o_4 = o_left, o_top + 62, width, height
        o_5 = o_left + 201, o_top + 62, width, height

        bbox_0 = o_left, o_top, o_left + width, o_top + height
        bbox_1 = o_left + 201, o_top, o_left + 201 + width, o_top + height
        bbox_2 = o_left, o_top + 31, o_left + width, o_top + 31 + height
        bbox_3 = o_left + 201, o_top + 31, o_left + 201 + width, o_top + 31 + height
        bbox_4 = o_left, o_top + 62, o_left + width, o_top + 62 + height
        bbox_5 = o_left + 201, o_top + 62, o_left + 201 + width, o_top + 62 + height

        regions = [o_0, o_1, o_2, o_3, o_4, o_5]
        bboxs = [bbox_0, bbox_1, bbox_2, bbox_3, bbox_4, bbox_5]

        screenshots_img = []
        screenshots_cv2 = []

        for i in range(len(regions)):
            # screenshot = pyautogui.screenshot(region=regions[i])
            screenshot = ImageGrab.grab(bbox=bboxs[i])
            screenshots_img.append(screenshot)

        # 是否在此处保存图片
        for i in range(len(screenshots_img)):
            screenshots_img[i].save("test/" + str(i) + ".png")

        for i in range(len(screenshots_img)):
            screenshots_cv2.append(cv2.cvtColor(
                np.array(screenshots_img[i]), cv2.COLOR_RGB2BGR))

        return screenshots_img, screenshots_cv2

    def get_options_names_by_pytesseract(self, screenshots):
        # 使用pytesseract来识别文字
        text_1 = its(screenshots[0]).rstrip('\n').rstrip('.').rstrip(',')
        text_2 = its(screenshots[1]).rstrip('\n').rstrip('.').rstrip(',')
        text_3 = its(screenshots[2]).rstrip('\n').rstrip('.').rstrip(',')
        text_4 = its(screenshots[3]).rstrip('\n').rstrip('.').rstrip(',')
        text_5 = its(screenshots[4]).rstrip('\n').rstrip('.').rstrip(',')
        text_6 = its(screenshots[5]).rstrip('\n').rstrip('.').rstrip(',')

        # 获取到选项文字
        option_names = [text_1, text_2, text_3, text_4, text_5, text_6]
        return option_names

    def get_options_names_by_features(self, screenshots):
        with open('options_feature_dict.json', 'r') as file:
            options_feature_dict = json.load(file)
        # print(screenshots)
        names = []
        for i in range(len(screenshots)):
            # print(screenshots[i])
            feature_vector = fun.get_optionimg_feature(screenshots[i])
            # print(feature_vector)
            option_name = fun.get_option_name_by_feature(
                feature_vector, options_feature_dict)
            names.append(option_name)
        return names

    def get_options_register_one(self, index, option_names, screenshots):
        num = 0
        for i in index:
            if option_names[i] != "":
                # print(screenshots[i])
                cv2.imwrite("./options/" +
                            option_names[i].replace('/', '') + ".png", screenshots[i])
                print("保存了", option_names[i])
            else:
                length = 20
                random_string = ''.join(random.choice(
                    string.ascii_letters + string.digits) for _ in range(length))
                cv2.imwrite("./options/" +
                            random_string + ".png", screenshots[i])

            num += 1
        # print("注册了", num, "个选项")

    def get_options_register(self, option_names, screenshots):
        for i in range(len(screenshots)):
            if option_names[i] != "":
                # print(screenshots[i])
                cv2.imwrite("./options/" +
                            option_names[i] + ".png", screenshots[i])
            else:
                length = 20
                random_string = ''.join(random.choice(
                    string.ascii_letters + string.digits) for _ in range(length))
                cv2.imwrite("./options/" +
                            random_string + ".png", screenshots[i])

        options_img_folder_path = './options'

        guns_feature_dict = {}

        num = 0

        for filename in os.listdir(options_img_folder_path):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):  # 仅处理图像文件，可以根据需要添加其他扩展名
                # 拼接完整的文件路径
                img_path = os.path.join(options_img_folder_path, filename)

                # 使用OpenCV读取图像
                img = cv2.imread(img_path)

                feature_vector = fun.get_optionimg_feature(img)

                guns_feature_dict[filename.strip(".png")] = feature_vector
                num += 1

        with open('options_feature_dict.json', 'w') as f:
            json.dump(guns_feature_dict, f)

        print("注册完成", "目前有", num, "为", round(num/265*100, 2), "%")

        # self.changeLabelText("注册完成", 'green')

    def mouse_auto_click(self, index):
        window_position = self.pos()
        t_left = window_position.x() + 10  # 左上角的 x 坐标
        t_top = window_position.y() + 315  # 左上角的 y 坐标

        # 鼠标点击坐标
        t_1 = t_left, t_top
        t_2 = t_left + 200, t_top
        t_3 = t_left, t_top + 30
        t_4 = t_left + 200, t_top + 30
        t_5 = t_left, t_top + 60
        t_6 = t_left + 200, t_top + 60

        target = [t_1, t_2, t_3, t_4, t_5, t_6]

        if index != -1:

            target_x, target_y = target[index][0], target[index][1]

            pyautogui.mouseDown(target_x, target_y)
            pyautogui.mouseUp(target_x, target_y)

        else:
            print("索引为-1")

        # pyautogui.moveTo(window_position.x() + 271,
        #                  window_position.y() + 237)

        pyautogui.moveTo(window_position.x() + 40,
                         window_position.y() + 240)

        # pyautogui.mouseDown(window_position.x() + 40,
        #                     window_position.y() + 240)
        # pyautogui.mouseUp(window_position.x() + 40,
        #                   window_position.y() + 240)

    def register(self, option_num):
        window_position = self.pos()
        left = window_position.x() + 90  # 左上角的 x 坐标
        top = window_position.y() + 49   # 左上角的 y 坐标
        right = window_position.x() + 237 + 90  # 右下角的 x 坐标
        bottom = window_position.y() + 49 + 158  # 右下角的 y 坐标

        gun_screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

        t_left = window_position.x() + 10  # 左上角的 x 坐标
        t_top = window_position.y() + 304  # 左上角的 y 坐标
        width = 180
        height = 20
        t_right = t_left + 199  # 右下角的 x 坐标
        t_bottom = t_top + 29  # 右下角的 y 坐标

        screenshot = ImageGrab.grab(
            bbox=(t_left, t_top, t_right, t_bottom))

        # 定义屏幕区域的坐标和大小
        r_1 = t_left, t_top, width, height
        r_2 = t_left + 200, t_top, width, height
        r_3 = t_left, t_top + 30, width, height
        r_4 = t_left + 200, t_top + 30, width, height
        r_5 = t_left, t_top + 60, width, height
        r_6 = t_left + 200, t_top + 60, width, height

        r = [r_1, r_2, r_3, r_4, r_5, r_6]

        # 使用pyautogui截取指定区域的屏幕截图
        screenshot = pyautogui.screenshot(region=r[option_num - 1])

        # 使用pytesseract来识别文字
        from pytesseract import image_to_string
        text = image_to_string(screenshot).rstrip('\n')
        text = text.replace('/', '')

        folder_path = './output_folder'
        file_path = os.path.join(folder_path, text + '.png')

        gun_screenshot.save(file_path)

        gun_img_folder_path = './output_folder'

        guns_feature_dict = {}

        num = 0

        for filename in os.listdir(gun_img_folder_path):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):  # 仅处理图像文件，可以根据需要添加其他扩展名
                # 拼接完整的文件路径
                img_path = os.path.join(gun_img_folder_path, filename)

                # 使用OpenCV读取图像
                img = cv2.imread(img_path)

                feature_vector = fun.get_gunimg_feature(img)

                guns_feature_dict[filename] = feature_vector
                num += 1

        with open('guns_feature_dict.json', 'w') as f:
            json.dump(guns_feature_dict, f)

        print("注册完成", text, "目前有", num, "为", round(num/266*100, 2), "%")

        self.changeLabelText("注册完成", 'green')

    def register_guns_from_files(self):
        gun_img_folder_path = './output_folder'

        guns_feature_dict = {}

        num = 0

        for filename in os.listdir(gun_img_folder_path):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):  # 仅处理图像文件，可以根据需要添加其他扩展名
                # 拼接完整的文件路径
                img_path = os.path.join(gun_img_folder_path, filename)

                # 使用OpenCV读取图像
                img = cv2.imread(img_path)

                feature_vector = fun.get_gunimg_feature(img)

                guns_feature_dict[filename[:-4]] = feature_vector
                num += 1

        with open('guns_feature_dict.json', 'w') as f:
            json.dump(guns_feature_dict, f)

        print("注册完成目前有", num, "为", round(num/265*100, 2), "%")

        self.changeLabelText("注册完成", 'green')

    def get_texts(self):
        window_position = self.pos()
        t_left = window_position.x() + 10  # 左上角的 x 坐标
        t_top = window_position.y() + 304  # 左上角的 y 坐标
        width = 180
        height = 20
        # t_right = t_left + 199  # 右下角的 x 坐标
        # t_bottom = t_top + 29  # 右下角的 y 坐标

        # screenshot = ImageGrab.grab(bbox=(t_left, t_top, t_right, t_bottom))

        # 保存图片
        # screenshot.save("screenshot_text.png")

        # 定义截图区域的坐标和大小
        r_1 = t_left, t_top, width, height
        r_2 = t_left + 200, t_top, width, height
        r_3 = t_left, t_top + 30, width, height
        r_4 = t_left + 200, t_top + 30, width, height
        r_5 = t_left, t_top + 60, width, height
        r_6 = t_left + 200, t_top + 60, width, height

        # 使用pyautogui截取指定区域的屏幕截图
        screenshot_1 = pyautogui.screenshot(region=r_1)
        screenshot_2 = pyautogui.screenshot(region=r_2)
        screenshot_3 = pyautogui.screenshot(region=r_3)
        screenshot_4 = pyautogui.screenshot(region=r_4)
        screenshot_5 = pyautogui.screenshot(region=r_5)
        screenshot_6 = pyautogui.screenshot(region=r_6)

        # 使用pytesseract来识别文字
        try:
            from pytesseract import image_to_string
            text_1 = image_to_string(screenshot_1)
            text_2 = image_to_string(screenshot_2)
            text_3 = image_to_string(screenshot_3)
            text_4 = image_to_string(screenshot_4)
            text_5 = image_to_string(screenshot_5)
            text_6 = image_to_string(screenshot_6)
            print("识别到的文字：", text_1, text_2, text_3, text_4, text_5, text_6)
        except ImportError:
            print("请先安装 pytesseract 库")

    def mousePressEvent(self, event):
        # 记录鼠标按下的位置
        if event.buttons() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        # 拖动窗口
        if self.drag_position is not None:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        # 释放鼠标
        self.drag_position = None

    def setRectColor(self):
        window_position = self.pos()
        x, y = window_position.x(), window_position.y() + 31
        screen = QApplication.primaryScreen()
        screenshot_l = screen.grabWindow(0, x, y, 400, 297)
        pixel_l = screenshot_l.toImage().pixel(200, 0)
        pixel_r = screenshot_l.toImage().pixel(0, 150)
        color_l = QColor(pixel_l)
        color_r = QColor(pixel_r)

        final_l_color = (color_l.red(), color_l.green(), color_l.blue())
        final_r_color = (color_r.red(), color_r.green(), color_r.blue())

        target_l, target_r = (84, 84, 84), (57, 57, 57)

        if euclidean_distance(final_l_color, target_l) + euclidean_distance(final_r_color, target_r) < 10:
            self.rect_color = Qt.green
            self.update()
        else:
            self.rect_color = Qt.white
            self.update()

    def get_pixel_color(self, pos):
        # 获取指定位置的像素颜色
        if self.screen_pixmap.isNull():
            return QColor()

        pixel = self.screen_pixmap.toImage().pixel(pos)
        return QColor(pixel)

    def keyPressEvent(self, event):
        # 按键事件处理函数
        step = 1  # 每次移动的像素步长

        if event.key() == Qt.Key_Left:
            self.move(self.x() - step, self.y())
        elif event.key() == Qt.Key_Right:
            self.move(self.x() + step, self.y())
        elif event.key() == Qt.Key_Up:
            self.move(self.x(), self.y() - step)
        elif event.key() == Qt.Key_Down:
            self.move(self.x(), self.y() + step)
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            self.setFocus()

    def paintEvent(self, event):
        # 在窗口上绘制一些内容（这里可以自定义绘制的内容）
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.rect_color)
        painter.drawRect(0, 0, 10, 10)

    def output_one(self):
        # 控制台输出数字1
        print(1)

    def move_window(self):
        # 获得焦点
        self.setFocus()

    def close_window(self):
        # 关闭窗口
        self.close()

    def changeLabelText(self, text, color='white'):
        # 在按钮点击时改变 Label 的文本
        self.label.setText(text)
        self.label.setStyleSheet("color: " + color + ";")

    def moveEvent(self, event):
        self.setRectColor()


def main():
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
