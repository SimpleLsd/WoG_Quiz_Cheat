import pyautogui

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
