#!/usr/bin/python
#coding=utf-8

import sys
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import QFileDialog
import sys
from time import sleep
import datetime
import MySQLdb
import json
import csv
import time
import shutil
import os
from PyQt4.QtGui import *

class Zhuanti(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(800, 300, 800, 600)
        self.setWindowTitle(u'模型工具模型专题处理')
        self.setWindowIcon(QtGui.QIcon('timg.jpg'))

        background = QtGui.QPixmap('background.jpg')
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(background))  # 添加背景图片
        self.setPalette(palette)

        self.upfile = QtGui.QPushButton(u'上传文件', self)
        self.upfile.setGeometry(300, 90, 200, 70)
        self.upfile.clicked.connect(self.button)

        self.download = QtGui.QPushButton(u'下载文件（请先上传文件）', self)
        self.download.setGeometry(300, 200, 200, 70)
        self.download.clicked.connect(self.button2)

        self.back = QtGui.QPushButton(u'后退', self)
        self.back.setGeometry(20, 20, 60, 40)
        self.back.clicked.connect(self.backbutton)

        self.file_name_result = "result_result_%s.csv" % time.strftime("%Y-%m-%d", time.localtime())
        self.file_name = ''

    def button2(self):
        if self.file_name:
            output_file_name = QtGui.QFileDialog.getExistingDirectory()
            if output_file_name:
                shutil.move(sys.path[0] + '\\' + self.file_name_result, output_file_name + '\\' + self.file_name_result)
        else:
            msg_box = QMessageBox(QMessageBox.Warning, u"提示", u"请先上传文件")
            msg_box.show()
            qe = QEventLoop()  # 阻塞
            qe.exec_()

    def button(self):
        self.file_name = QFileDialog.getOpenFileName(self, 'Open file','.',"csv files (*.csv)")
        print self.file_name
        return
        if self.file_name:
            self.main(self.file_name)

    def backbutton(self):
        self.close()

    def main(self,file_name):

        with open(file_name, 'r') as fd:
            reader = fd.readlines()
        lists = []
        num = 0
        s_all = ""
        s_other = ""
        for line in reader:
            line = line.decode("gbk")
            line = line.split(',')
            if u"其他" in line[0]:
                s_all = line[1]
            else:
                s_other += line[1]
        print "=============", s_all
        s_all_lists = s_all.split(' ')
        s_all_lists = [x.strip() for x in s_all_lists if x.strip()]
        s_all_lists = list(set(s_all_lists))

        s_other_lists = s_other.split(' ')
        s_other_lists = [x.strip() for x in s_other_lists if x.strip()]
        s_other_lists = list(set(s_other_lists))

        lists_left = list(set(s_all_lists) & set(s_other_lists))
        lists_left = self.paixu(lists_left)
        for line in reader:
            line = line.decode("gbk")
            line = line.split(',')
            if u"其他" in line[0]:
                s_left = self.s2_words_before(line[1], lists_left)
                lists.append([(line[0].encode("utf8"), s_left.encode("utf8"))])
                break
            else:
                print line[0]
        for line in reader:
            line = line.decode("gbk")
            line = line.split(',')
            if u"其他" not in line[0]:
                s_left = self.s2_words_before(line[1], lists_left)
                lists.append([(line[0].encode("utf8"), s_left.encode("utf8"))])

            """
            col_num = len(line)
            if not num:
                num += 1
                tup1 = ()
                for i in range(col_num):
                    tup1 += (line[i],)
                ll = [(tup1)]
                lists.append(ll)
                continue
            num += 1
            s_all = line[0]
            s_all_lists = s_all.split(' ')
            s_all_lists = [x.strip() for x in s_all_lists if x.strip()]
            s_all_lists = list(set(s_all_lists))
            s_other = ""
            for i in range(1,col_num):
                s_other +=  (line[i]+' ')
            s_other_lists = s_other.split(' ')
            s_other_lists = [x.strip() for x in s_other_lists if x.strip()]
            s_other_lists = list(set(s_other_lists))
            lists_left = list(set(s_all_lists) & set(s_other_lists))
            lists_left = paixu(lists_left)
            s_left = s2_words_before(s_all,lists_left)
            tup = (s_left,)
            for i in range(1,col_num):
                line[i] = s2_words_before(line[i],lists_left)
                tup += (line[i],)
            l = [(tup)]
            lists.append(l)
            """
        # csvfile.close()

        if lists:
            self.csv_write(lists, False)

    def paixu(self,words_false):
        """
        替换的时候需要先替换长词，再替换短词，否则替换会出问题
        """
        false_length = len(words_false)
        for i in range(false_length - 1):
            for j in range(i + 1, false_length):
                if len(words_false[i]) < len(words_false[j]):
                    temp_key = words_false[j]
                    words_false[j] = words_false[i]
                    words_false[i] = temp_key
        return words_false

    def s2_words_before(self,s, lists):
        """
        包含关系中的词提前
        先判断词语中是否有此关键词，再确定提前词的统计
        """
        l = []
        for i in lists:
            if i in s:
                l.append(i)
                s = s.replace(i, '')
        ss = ""
        for i in lists:
            if i in l:
                ss += (i + ' ')
        s = ss + "#####" + s

        return s

    def csv_write(self,info_lists, is_dict=True):
        '''
        writer
        根据字典列表写入csv
        可处理csv_write_dic()能处理的格式  [{a:1, b:2}, {a:2, b:3}]
        还可处理非字典形式  [(1,2),(2,3)]
        '''
        print u"**********正在写入到文件中,请稍等···**********"

        length = len(info_lists)
        if length > 500:
            s_time = 0.001
        elif length > 200:
            s_time = 0.05
        else:
            s_time = 0.1
        output = sys.stdout
        start = 0
        step = 100.0 / length
        writer = csv.writer(open(self.file_name_result, "wb"))
        for info_list in info_lists:
            if isinstance(info_list, dict):
                info_list = [info_list]
                print 111
            if is_dict:
                keys = info_list[0].keys()
                # 写入第一行
                print keys
                writer.writerow(keys)
                code = compile("line = [info.get(key,'') for key in keys]", "", "exec")
            else:
                code = compile("line = list(info)", "", "exec")
            for info in info_list:
                exec code
                writer.writerow(line)
            start = start + step
            sleep(s_time)
            output.write('\rcomplete percent:%.0f%%' % start)
        output.flush()

        return

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    home = Zhuanti()
    home.show()
    sys.exit(app.exec_())