#!/usr/bin/python
#coding=utf-8

import sys
from PyQt4 import QtGui,QtCore
import Auto_report
from yiliao_output import Output
from zhuanti import Zhuanti
from add_delete import Add_delete


class Home(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(800, 300, 800, 600)
        self.setWindowTitle(u'模型工具_V 1.0.0')
        self.setWindowIcon(QtGui.QIcon('timg.jpg'))

        background = QtGui.QPixmap('background.jpg')
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(background))  # 添加背景图片
        self.setPalette(palette)

        # self.button1 = QtGui.QPushButton(u'CSV文件换行符处理', self)
        # self.button1.setGeometry(300, 40, 200, 70)
        # self.page1 = Csv()
        # self.button1.clicked.connect(self.on_button1)

        self.button2 = QtGui.QPushButton(u'自动化生成正负面报告', self)
        self.button2.setGeometry(300, 50, 200, 70)
        self.page2 = Auto_report.Report()
        self.button2.clicked.connect(self.on_button2)
        # self.connect(self.button2, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))

        self.button3 = QtGui.QPushButton(u'医疗数据导出', self)
        self.button3.setGeometry(300, 180, 200, 70)
        self.page3 = Output()
        self.button3.clicked.connect(self.on_button3)

        self.button4 = QtGui.QPushButton(u'模型专题处理', self)
        self.button4.setGeometry(300, 310, 200, 70)
        self.page4 = Zhuanti()
        self.button4.clicked.connect(self.on_button4)

        self.button5 = QtGui.QPushButton(u'包含关系', self)
        self.button5.setGeometry(300, 440, 200, 70)
        self.page5 = Add_delete()
        self.button5.clicked.connect(self.on_button5)


    # def on_button1(self):
    #     self.close()
    #     self.page1.show()


    def on_button2(self):
        self.page2.show()

    def on_button3(self):
        # self.close()
        self.page3.show()

    def on_button4(self):
        # self.close()
        self.page4.show()

    def on_button5(self):
        # self.close()
        self.page5.show()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    home = Home()
    home.show()
    sys.exit(app.exec_())
