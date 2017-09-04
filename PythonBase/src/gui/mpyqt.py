#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:python gui之pyqt学习
    Ref:http://mp.weixin.qq.com/s/Ru_TpOnelMXPzH-1o34oZw
    State：
    Date:2017/5/17
    Author:tuling56
'''
import re, os, sys
import hues

reload(sys)
sys.setdefaultencoding('utf-8')


from PyQt4 import QtGui, QtCore
import httplib
from urllib import urlencode


def out(text):
    p = re.compile(r'","')
    m = p.split(text)
    result = unicode(m[0][4:].decode('utf-8'))
    DS_Widget.setDS_TextEdit_text(result)


def dic():
    word = DS_Widget.getDS_LineEdit_text()
    text = urlencode({'text': word})
    h = httplib.HTTP('translate.google.cn')
    h.putrequest('GET', '/translate_a/t?client=t&hl=zh-CN&sl=en&tl=zh-CN&ie=UTF-8&oe=UTF-8&' + text)
    h.endheaders()
    h.getreply()
    f = h.getfile()
    lines = f.readlines()
    out(lines[0])
    f.close()


class DS_QWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.DS_LineEdit = QtGui.QLineEdit(self)
        DS_SearchButton = QtGui.QPushButton('Search', self)
        self.DS_TextEdit = QtGui.QTextEdit(self)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.DS_LineEdit)
        hbox.addWidget(DS_SearchButton)

        vbox = QtGui.QVBoxLayout(self)
        vbox.addLayout(hbox)
        vbox.addWidget(self.DS_TextEdit)

        self.resize(500, 300)
        self.setWindowTitle('Dictionary')
        self.connect(DS_SearchButton, QtCore.SIGNAL('clicked()'), dic)
        self.setLayout(vbox)

    def getDS_LineEdit_text(self):
        return self.DS_LineEdit.text()

    def setDS_TextEdit_text(self, text):
        self.DS_TextEdit.setText(text)


if __name__ == "__main__":
    DS_APP = QtGui.QApplication(sys.argv)
    DS_Widget = DS_QWidget()
    DS_Widget.show()
    sys.exit(DS_APP.exec_())
