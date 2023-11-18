from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
import sys
import chardet      # 格式检测
import os

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Color = ''
        self.Size = ''
        self.Type = ''

        # 隐藏窗体标题
        self.setWindowFlag(Qt.FramelessWindowHint)
        # 将窗体始终显示在最前端
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        # 设置窗体标题
        self.setWindowTitle("Text Review")
        # 设置整个窗体透明度，数值范围0 ~ 1（0为完全透明，也就是看不见窗体及内部控件）
        # self.setWindowOpacity(0.5)
        # 设置窗体为透明背景，但内部控件不受影响
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # 设置窗体位置及大小
        self.setGeometry(0, 0, 1800, 200)

        # 创建一个Qlabel
        self.TextLabel = QLabel('上下键翻页', self)
        self.TextLabel.resize(1800, 200)
        self.TextLabel.setAlignment(Qt.AlignCenter)
        # 设置Qlabel背景色
        # self.TextLabel.setStyleSheet("background-color: lightgreen;")
        self.TextLabel.setStyleSheet("background-color: transparent;")

        # 读取配置文件
        self.ReadConfig()

        font = QFont()
        font.setBold(True)
        font.setPixelSize(int(self.Size))   # 字体大小
        font.setFamily(self.Type)           # 字体
        self.TextLabel.setFont(font)
        self.TextLabel.setStyleSheet(self.Color)    # 字体颜色

        # 移动窗口位置
        self.MoveWindow()
        # show all the widgets
        self.show()

    # 移动窗口位置
    def MoveWindow(self):
        # 获取屏幕的尺寸信息
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口的尺寸信息
        size = self.geometry()
        # 将窗口移动到指定位置
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    # 窗体标题栏隐藏后，窗口无法拖动，可通过改写以下两个鼠标事件来实现窗体移动
    def mousePressEvent(self, event):
        # 记录鼠标按下时的位置
        self.offset = event.pos()
        # 显示Qlabel背景色
        self.TextLabel.setStyleSheet("background-color: lightgreen;")

    def mouseReleaseEvent(self, event):
        # 恢复透明色
        self.TextLabel.setStyleSheet("background-color: transparent;")
        # 由于移动时被选中，所以这里需要重新恢复Qlabel字体颜色
        self.TextLabel.setStyleSheet(self.Color)  # 字体颜色

    def mouseMoveEvent(self, event):
        # 移动窗口位置
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)

    def ReadConfig(self):
        # 检测ini文件是否存在
        if os.path.exists('./config.ini'):
            # 检测ini文件编码格式
            TextCode = open('./config.ini', 'rb')
            temp = TextCode.read()
            info = chardet.detect(temp)
            # print(info)
            # print(temp.decode(info['encoding']))
            TextCode.close()

            # 用检测到的格式打开ini文档
            CurFile = open('./config.ini', 'r', encoding=info['encoding'])
            # 读取文件内容
            self.Color = CurFile.readline()
            self.Size = CurFile.readline()
            self.Type = CurFile.readline()
            CurFile.close()
        else:
            CurFile = open('./config.ini', 'w', encoding='utf-8')
            CurFile.write('color:#FE00FE;' + '\n')
            CurFile.write('30' + '\n')
            CurFile.write('等线' + '\n')
            CurFile.close()
            self.Color = 'color:#FE00FE;'
            self.Size = '30'
            self.Type = '等线'

    # 键盘某个键被按下时调用
    def keyPressEvent(self, QKeyEvent):
        global CurFileText, CurFileText_line, CurFileText_Nums

        self.TextLabel.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        # 按键处理
        if QKeyEvent.key() == Qt.Key_Up:    # 向上翻一行
            if CurFileText_line == 0:
                CurFileText_line = CurFileText_Nums - 1
            else:
                CurFileText_line = CurFileText_line -1
            self.TextLabel.setText(CurFileText[CurFileText_line])
        elif QKeyEvent.key() == Qt.Key_Down:    # 向下翻一行
            if self.TextLabel.text() != 'Ready Go!':
                if CurFileText_line == CurFileText_Nums - 1:
                    CurFileText_line = 0
                else:
                    CurFileText_line = CurFileText_line + 1
            self.TextLabel.setText(CurFileText[CurFileText_line])
        elif QKeyEvent.key() == Qt.Key_Space:   # 向下翻五行
            CurFileText_line = CurFileText_line + 5
            if CurFileText_line >= CurFileText_Nums:
                CurFileText_line = CurFileText_Nums - 1
            self.TextLabel.setText(CurFileText[CurFileText_line])
        elif QKeyEvent.key() == Qt.Key_Escape:   # 关闭程序
            App.quit()

# create pyqt5 app
App = QApplication(sys.argv)
# create the instance of our Window
window = Window()

# 检测txt文件编码格式
TextCode = open('./doc.txt', 'rb')
temp = TextCode.read()
info = chardet.detect(temp)
# print(info)
# print(temp.decode(info['encoding']))
TextCode.close()

# 用检测到的格式打开txt文档
CurFile = open('./doc.txt', 'r', encoding=info['encoding'])
CurFileText = []
# 读取文件内容
i = True
while i:
    temp_line = CurFile.readline()
    if temp_line:
        CurFileText.append(temp_line)
    else:
        i = False
        CurFile.close()
# 获取总行数并将当前行置为0
CurFileText_Nums = len(CurFileText)
CurFileText_line = 0
# print(CurFileText_Nums)

# Start the App
sys.exit(App.exec())

