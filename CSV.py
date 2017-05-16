# #!/usr/bin/python
# #coding=utf-8
#
# import sys
# from PyQt4 import QtGui,QtCore
#
# class Csv(QtGui.QWidget):
#     def __init__(self, parent = None):
#         QtGui.QWidget.__init__(self, parent)
#         self.setGeometry(800, 300, 800, 600)
#         self.setWindowTitle(u'模型工具CSV文件换行符处理')
#         self.setWindowIcon(QtGui.QIcon('timg.jpg'))
#
# if __name__ == '__main__':
#     app = QtGui.QApplication(sys.argv)
#     home = Csv()
#     home.show()
#     sys.exit(app.exec_())




# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os
import time

class Test(QDialog):
    def __init__(self,parent=None):
        super(Test,self).__init__(parent)
        self.listFile=QListWidget()
        self.btnStart=QPushButton('Start')
        layout=QGridLayout(self)
        layout.addWidget(self.listFile,0,0,1,2)
        layout.addWidget(self.btnStart,1,1)
        self.connect(self.btnStart,SIGNAL('clicked()'),self.slotAdd)
    def slotAdd(self):
        for n in range(10):
            str_n='File index {0}'.format(n)
            self.listFile.addItem(str_n)
            QApplication.processEvents()
            time.sleep(1)
app=QApplication(sys.argv)
dlg=Test()
dlg.show()
sys.exit(app.exec_())


