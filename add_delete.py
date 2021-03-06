#!/usr/bin/python
#coding=utf-8

import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import *
import chardet
import time

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

        # self.before_path_name = 'C:/Users/Administrator/Desktop/model_PyQt/all_of_the_aaaaaaaaaaaaaaaaaaaa/before_after/words_add_delete/words_before.txt'
        # self.after_path_name  = 'C:/Users/Administrator/Desktop/model_PyQt/all_of_the_aaaaaaaaaaaaaaaaaaaa/before_after/words_add_delete/words_after.txt'
        self.before_path_name = ''
        self.after_path_name = ''

        gridlayout.setRowMinimumHeight(3, 500)


        label = QtGui.QLabel(u'删除数据量')  # 创建标签
        label.setAlignment(QtCore.Qt.AlignCenter)
        gridlayout.addWidget(label, 1, 0)
        self.edit1 = QtGui.QTextEdit()  # 创建多行文本框
        self.edit1.setText('删除数据量'.decode('utf8'))  # 设置文本框中的文字
        gridlayout.addWidget(self.edit1, 2, 0, 1, 1)
        self.setLayout(gridlayout)

        self.edit11 = QtGui.QTextEdit()  # 创建多行文本框
        self.edit11.setText('删除数据量'.decode('utf8'))  # 设置文本框中的文字
        gridlayout.addWidget(self.edit11,3,0,8,1)
        self.setLayout(gridlayout)

        labe2 = QtGui.QLabel(u'增加数据量')  # 创建标签
        labe2.setAlignment(QtCore.Qt.AlignCenter)
        gridlayout.addWidget(labe2, 1, 1)
        self.edit2 = QtGui.QTextEdit()  # 创建多行文本框
        self.edit2.setText('增加数据量'.decode('utf8'))  # 设置文本框中的文字
        gridlayout.addWidget(self.edit2, 2, 1, 1, 1)
        self.setLayout(gridlayout)

        self.edit22 = QtGui.QTextEdit()  # 创建多行文本框
        self.edit22.setText('增加数据量'.decode('utf8'))  # 设置文本框中的文字
        gridlayout.addWidget(self.edit22, 3, 1, 8, 1)
        self.setLayout(gridlayout)

        labe3 = QtGui.QLabel(u'相同数据量')  # 创建标签
        labe3.setAlignment(QtCore.Qt.AlignCenter)
        gridlayout.addWidget(labe3, 1, 2)
        self.edit3 = QtGui.QTextEdit()  # 创建多行文本框
        self.edit3.setText('相同数据量'.decode('utf8'))  # 设置文本框中的文字
        gridlayout.addWidget(self.edit3, 2, 2, 1, 1)
        self.setLayout(gridlayout)

        self.edit33 = QtGui.QTextEdit()  # 创建多行文本框
        self.edit33.setText('相同数据量'.decode('utf8'))  # 设置文本框中的文字
        gridlayout.addWidget(self.edit33, 3, 2, 8, 1)
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

    def sort(self,mdzz):
        n= 0
        while n<len(mdzz):
            for i in range(0,len(mdzz)):
                if i<len(mdzz)-1:
                    if len(mdzz[i])>len(mdzz[i+1]):
                        # print mdzz[i],mdzz[i+1]
                        mdzz[i],mdzz[i+1] = mdzz[i+1],mdzz[i]
                # print mdzz
            n+=1
        return mdzz


    def main(self):
        t1 = time.time()

        l_before_list = self.get_txt_words_list(self.before_path_name)
        l_after_list = self.get_txt_words_list(self.after_path_name)

        delete_list = set(l_before_list) - set(l_after_list)
        length_delete = len(delete_list)
        print u"删除数据量：%s" % length_delete

        delete_list = self.sort(list(delete_list))

        text1 = ''
        for aaa in delete_list:
            text1 = text1 + aaa + '\n'
        text1 = text1.decode("gbk").encode("utf-8")
        # print chardet.detect(text1)
        # print chardet.detect( "删除数据量：")
        # text1 = "删除数据量：%s" % length_delete + '\n\n' + text1
        text11 = "删除数据量：%s" % length_delete
        # print text1
        # print chardet.detect(text1)
        self.edit1.setText(text11.decode('utf-8'))
        self.edit11.setText(text1.decode('utf-8'))

        add_list = set(l_after_list) - set(l_before_list)
        length_add = len(add_list)
        print u"增加数据量：%s" % length_add

        add_list = self.sort(list(add_list))

        text2 = ''
        for bbb in add_list:
            text2 = text2 + bbb + '\n'
        text2 = text2.decode("gbk").encode("utf-8")
        # text2 = "增加数据量：%s" % length_add + '\n\n' + text2
        text22 = "增加数据量：%s" % length_add
        self.edit2.setText(text22.decode('utf-8'))
        self.edit22.setText(text2.decode('utf-8'))

        jiaoji = set(l_after_list) & set(l_before_list)
        length_jiaoji = len(jiaoji)
        print u"相同数据量：%s" % length_add

        jiaoji = self.sort(list(jiaoji))

        text3 = ''
        for ccc in jiaoji:
            text3 = text3 + ccc + '\n'
        text3 = text3.decode("gbk").encode("utf-8")
        # text3 = "相同数据量：%s" % length_add + '\n\n' + text3
        text33 = "相同数据量：%s" % length_add
        self.edit3.setText(text33.decode('utf-8'))
        self.edit33.setText(text3.decode('utf-8'))

        self.before_path_name = ''
        self.after_path_name = ''

        print u"ACHIEVE"

        t2 = time.time()
        print float(t2-t1)

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


    # a = ['aa','a','aaaaaaaaaaa','aaaa','aaa','aaaaa']
    # b = home.sort(a)
    # print b
