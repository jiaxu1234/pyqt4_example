#!/usr/bin/python
#coding=utf-8

import sys
from PyQt4 import QtGui,QtCore
from time import sleep
import datetime
import MySQLdb
import json
import csv
import difflib
import time
import shutil
from PyQt4.QtGui import *
import time

class Output(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(800, 300, 800, 600)
        self.setWindowTitle(u'模型工具医疗数据导出')
        self.setWindowIcon(QtGui.QIcon('timg.jpg'))

        background = QtGui.QPixmap('background.jpg')
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(background))  # 添加背景图片
        self.setPalette(palette)

        self.cal = QtGui.QCalendarWidget(self)
        # self.cal.setGridVisible(True)
        self.cal.setGeometry(250, 50, 300, 180)
        self.connect(self.cal, QtCore.SIGNAL('selectionChanged()'), self.select)

        self.output = QtGui.QPushButton(u'一键导出', self)
        self.output.setGeometry(300, 230, 200, 70)
        self.output.clicked.connect(self.button)

        self.back = QtGui.QPushButton(u'后退', self)
        self.back.setGeometry(20, 20, 60, 40)
        self.back.clicked.connect(self.backbutton)

        self.mysql_conn = MySQLdb.connect(
            host='192.168.16.68',
            port=3306,
            user='root',
            passwd='duamiawen&&&&',
            db='test1',
            charset='utf8'
        )
        self.cursor = self.mysql_conn.cursor()
        # content_length = 500  #设置内容的长度
        self.content_length = -1  # 设置内容的长度
        self.url_dic = {}  # 相似度超过阈值的链接value设置为1
        self.url_likes_lists = {}  # 存储相似度超过阈值的链接  {'url':[url1,url2,url3,...]}

        self.crawled_time = ''

        # self.crawled_time = time.strftime("%Y-%m-%d", time.localtime())
        # crawled_time = (datetime.datetime.now()-datetime.timedelta(1)).strftime('%Y-%m-%d')  # 采集时间为昨天  参数1可以修改，代表几天前
        # crawled_time = '2017-05-12'  # 直接标注某天

    def select(self):
        self.crawled_time = self.cal.selectedDate()
        self.crawled_time = str(self.crawled_time.toPyDate())
        print self.crawled_time

    def button(self):
        if self.crawled_time:
            file_path = QtGui.QFileDialog.getExistingDirectory()
            print file_path
            if file_path:
                self.main(file_path)
                # print file_name
        else:
            msg_box = QMessageBox(QMessageBox.Warning, u"提示", u"请在上方日历中选择所需导出数据的日期")
            msg_box.show()
            qe = QEventLoop()  # 阻塞
            qe.exec_()

    def backbutton(self):
        self.close()


    def main(self,file_path):
        t1 = time.time()

        data_types = ['yiliao']
        print u"*************程序运行中,请稍等···*************\n"
        for data_type in data_types:
            file_name = 'model_info_%s_%s.csv' % (data_type,self.crawled_time)  # 生成的csv文件名称
            mysql_name = 'model_info_%s' % data_type  # 医疗信息表
            file_like_name = 'model_info_like_%s_%s.csv' % (data_type,self.crawled_time)  # 医疗信息表

            print self.crawled_time
            lists, url_likes = self.data_out(mysql_name, self.crawled_time)
            if lists:
                self.csv_write(lists, file_name, False)
            if url_likes:
                self.csv_write(url_likes, file_like_name, False)
                # 所有数据flag置为0
                # sql = 'update %s set flag="0"'%mysql_name
                # cursor.execute(sql)
        print u"*************恭喜您,数据全部写入完毕*************"
        # self.cursor.close()
        # self.mysql_conn.close()

        shutil.move(sys.path[0] + '\\' + file_name, file_path + '\\' + file_name)

        t2 = time.time()
        print float(t2-t1)

    def data_out(self,mysql_name, crawled_time):
        d_type = mysql_name.split('_')[-1]
        lists = [[('url', 'crawled', 'title', "source", "content")]]  # 表头

        # 查找医疗信息,时间为当天时间
        sql = 'select * from %s where crawled like "%s%%" and flag="0" order by crawled DESC' % (mysql_name, crawled_time)
        print sql
        # 查找医疗信息,信息为还没有导出过的数据
        # sql = 'select * from %s where flag="0"'%mysql_name
        self.cursor.execute(sql)
        infos = self.cursor.fetchall()
        length = len(infos)
        if length == 0:
            print u"没有新数据"

            msg_box = QMessageBox(QMessageBox.Warning, u"提示", u"没有符合条件的数据")
            msg_box.show()
            qe = QEventLoop()  # 阻塞
            qe.exec_()

            return [], []
        if length > 500:
            s_time = 0.001
        elif length > 200:
            s_time = 0.05
        else:
            s_time = 0.1
        print u"***************一共查询到%s条%s信息***************\n" % (length, d_type)
        print u"**********正在查询%s数据,请稍等···**********\n" % d_type
        output = sys.stdout
        start = 0
        step = 100.0 / length
        for info in infos:
            url = info[0].encode("utf8")
            like_flag = self.url_dic.get(url, 0)
            if like_flag:
                # print u"此条信息为相似信息,不导出"
                sql = 'update %s set flag="0" where url="%s"' % (mysql_name, url)  # 测试时改为0，不改为4
                self.cursor.execute(sql)
                continue
            try:
                crawled = info[1].encode("utf8")
            except:
                crawled = ''
            if info[2]:
                title = info[2].encode("utf8")
            else:
                title = ''
            source = info[3].encode("utf8")
            if info[4]:
                try:
                    content = title + (info[4].replace('\r', ' ').replace('\n', ' ').replace("\t", " "))[
                                      0:content_length].encode("utf8")
                except Exception as e:
                    content = ''
            else:
                content = ''
            url_likes_list = []
            aa = 0
            for info in infos:  # 与导出的其他数据进行title的相似度比较
                aa += 1
                url_next = info[0].encode("utf8")
                if url == url_next:
                    continue
                if info[2]:
                    title_next = info[2].encode("utf8")
                else:
                    title_next = ''
                if info[4]:
                    content_next = info[4].encode("utf8")
                else:
                    content_next = ''
                like = difflib.SequenceMatcher(None, title, title_next).ratio()

                if like > 0.5:  # 阈值
                    like = difflib.SequenceMatcher(None, content, content_next).ratio()
                    if like > 0.7:
                        self.url_dic[url_next] = 1
                        url_likes_list.append(url_next)
            if url_likes_list:
                self.url_likes_lists[url] = url_likes_list
            l = [(url, crawled, title, source, content)]
            lists.append(l)
            start = start + step
            sleep(s_time)
            output.write('\rcomplete percent:%.0f%%' % start)
            sql = 'update %s set flag="0" where url="%s"' % (mysql_name, url)  # 测试时改为0，不改为1
            self.cursor.execute(sql)
        output.flush()
        print '\n'
        # 把存储好的相似度相近链接转换成写csv格式
        url_likes = []
        if self.url_likes_lists:
            url_likes = [[('链接/导出', '相似链接/未导出')]]
            for k, v in self.url_likes_lists.iteritems():
                num = 1
                for like_url in v:
                    if num:
                        url_likes.append([(k, like_url)])
                        num = 0
                    else:
                        l_u = [('', like_url)]
                        url_likes.append(l_u)
        return lists, url_likes

    def csv_write(self,info_lists, file_name='', is_dict=True):
        '''
        writer
        根据字典列表写入csv
        可处理csv_write_dic()能处理的格式  [{a:1, b:2}, {a:2, b:3}]
        还可处理非字典形式  [(1,2),(2,3)]
        '''
        print u"**********正在写入到文件中,请稍等···**********"
        if not file_name:
            file_name = 'model_info_yiliao.csv'
        d_type = file_name.split('_')[-1].replace('.csv', '')
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
        writer = csv.writer(open(file_name, "wb"))
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
        print u"\n恭喜您,%s数据写入成功\n" % d_type
        return



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    home = Output()
    home.show()
    sys.exit(app.exec_())