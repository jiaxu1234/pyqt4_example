#!/usr/bin/python
#coding=utf-8

import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import *
import chardet

class Add_delete(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(800, 300, 800, 600)
        self.setWindowTitle(u'模型工具包含关系')
        self.setWindowIcon(QtGui.QIcon('timg.jpg'))

        background = QtGui.QPixmap('background.jpg')
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(background))  # 添加背景图片
        self.setPalette(palette)

        gridlayout = QtGui.QGridLayout()  # 创建布局组件
        self.input1 = QtGui.QPushButton(u'导入处理前txt文件', self)
        self.input1.setGeometry(30, 10, 200, 30)
        gridlayout.addWidget(self.input1, 0, 0)
        self.input1.clicked.connect(self.button1)

        self.input2 = QtGui.QPushButton(u'导入处理后txt文件', self)
        self.input2.setGeometry(290, 10, 200, 30)
        gridlayout.addWidget(self.input2, 0, 1)
        self.input2.clicked.connect(self.button2)

        self.set = QtGui.QPushButton(u'进行比较', self)
        self.set.setGeometry(550, 10, 200, 30)
        gridlayout.addWidget(self.set, 0, 2)
        self.set.clicked.connect(self.button3)

        self.before_path_name = 'C:/Users/Administrator/Desktop/model_PyQt/before_after/words_add_delete/words_before.txt'
        self.after_path_name  = 'C:/Users/Administrator/Desktop/model_PyQt/before_after/words_add_delete/words_after.txt'
        self.before_path_name = ''
        self.after_path_name = ''


        label = QtGui.QLabel(u'删除数据量')  # 创建标签
        label.setAlignment(QtCore.Qt.AlignCenter)
        gridlayout.addWidget(label, 1, 0)
        self.edit1 = QtGui.QTextEdit()  # 创建多行文本框
        self.edit1.setText('删除数据量'.decode('utf8'))  # 设置文本框中的文字
        gridlayout.addWidget(self.edit1, 2, 0)
        self.setLayout(gridlayout)

        labe2 = QtGui.QLabel(u'增加数据量')  # 创建标签
        labe2.setAlignment(QtCore.Qt.AlignCenter)
        gridlayout.addWidget(labe2, 1, 1)
        self.edit2 = QtGui.QTextEdit()  # 创建多行文本框
        self.edit2.setText('增加数据量'.decode('utf8'))  # 设置文本框中的文字
        gridlayout.addWidget(self.edit2, 2, 1)
        self.setLayout(gridlayout)

        labe3 = QtGui.QLabel(u'相同数据量')  # 创建标签
        labe3.setAlignment(QtCore.Qt.AlignCenter)
        gridlayout.addWidget(labe3, 1, 2)
        self.edit3 = QtGui.QTextEdit()  # 创建多行文本框
        self.edit3.setText('相同数据量'.decode('utf8'))  # 设置文本框中的文字
        gridlayout.addWidget(self.edit3, 2, 2)
        self.setLayout(gridlayout)

    def button1(self):
        self.before_path_name = QFileDialog.getOpenFileName(self, 'Open file', '.', "txt files (*.txt)")
        print self.before_path_name


    def button2(self):
        self.after_path_name = QFileDialog.getOpenFileName(self, 'Open file', '.', "txt files (*.txt)")
        print self.after_path_name

    def button3(self):
        if self.before_path_name and self.after_path_name:
            print '--import success--'
            self.main()
        elif not self.before_path_name:
            msg_box = QMessageBox(QMessageBox.Warning, u"提示", u"请上传处理前文件")
            msg_box.show()
            qe = QEventLoop()  # 阻塞
            qe.exec_()
        elif not self.after_path_name:
            msg_box = QMessageBox(QMessageBox.Warning, u"提示", u"请上传处理后文件")
            msg_box.show()
            qe = QEventLoop()  # 阻塞
            qe.exec_()

    def main(self):
        l_before_list = self.get_txt_words_list(self.before_path_name)
        l_after_list = self.get_txt_words_list(self.after_path_name)

        delete_list = set(l_before_list) - set(l_after_list)
        length_delete = len(delete_list)
        print u"删除数据量：%s" % length_delete

        text1 = ''
        for aaa in delete_list:
            text1 = text1 + aaa + '\n'
        text1 = text1.decode("gbk").encode("utf-8")
        # print chardet.detect(text1)
        # print chardet.detect( "删除数据量：")
        text1 = "删除数据量：%s" % length_delete + '\n\n' + text1
        # print text1
        # print chardet.detect(text1)
        self.edit1.setText(text1.decode('utf-8'))

        add_list = set(l_after_list) - set(l_before_list)
        length_add = len(add_list)
        print u"增加数据量：%s" % length_add
        text2 = ''
        for bbb in add_list:
            text2 = text2 + bbb + '\n'
        text2 = text2.decode("gbk").encode("utf-8")
        text2 = "增加数据量：%s" % length_add + '\n\n' + text2
        self.edit2.setText(text2.decode('utf-8'))

        jiaoji = set(l_after_list) & set(l_before_list)
        length_jiaoji = len(jiaoji)
        print u"相同数据量：%s" % length_add
        text3 = ''
        for ccc in jiaoji:
            text3 = text3 + ccc + '\n'
        text3 = text3.decode("gbk").encode("utf-8")
        text3 = "相同数据量：%s" % length_add + '\n\n' + text3
        self.edit3.setText(text2.decode('utf-8'))

        self.before_path_name = ''
        self.after_path_name = ''

        print u"ACHIEVE"

    def get_txt_words_list(self,file_name):
        with open(file_name, 'r') as fd:
            l_before = fd.read()
        l_before_str = l_before.replace('\n', ' ')
        l_before_list = l_before_str.split(' ')
        l_before_list = [x.strip() for x in l_before_list if x.strip()]
        return l_before_list

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    home = Add_delete()
    home.show()
    sys.exit(app.exec_())