import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt


class ColorChangerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Color Changer')

        self.rect_color = Qt.white  # 初始颜色为白色

        change_color_btn = QPushButton('修改颜色', self)
        change_color_btn.setGeometry(150, 250, 100, 30)
        change_color_btn.clicked.connect(self.changeRectangleColor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.rect_color)
        painter.drawRect(0, 0, 10, 10)

    def changeRectangleColor(self):
        # 修改矩形的颜色
        if self.rect_color == Qt.white:
            self.rect_color = Qt.red  # 改为红色
        else:
            self.rect_color = Qt.white  # 改回白色

        # 请求重新绘制
        self.update()


def main():
    app = QApplication(sys.argv)
    window = ColorChangerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
