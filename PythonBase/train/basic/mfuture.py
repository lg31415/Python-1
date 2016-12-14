#!/usr/bin/env python
# -*- coding: utf8 -*-
from  __future__ import  division,unicode_literals
#值得注意的是若适用Python3的编码模块，则以上语句必须放在文件的最前面
__author__ = 'yjm'
'''
  功能注释：
'''

def mstrcoding():
    print '\'xxx\' is unicode?', isinstance('xxx', unicode)
    print 'u\'xxx\' is unicode?', isinstance(u'xxx', unicode)
    print '\'xxx\' is str?', isinstance('xxx', str)
    print 'b\'xxx\' is str?', isinstance(b'xxx', str)


def mdivision():
    print '10 / 3 =', 10 / 3
    print '10.0 / 3 =', 10.0 / 3
    print '10 // 3 =', 10 // 3


if __name__ == "__main__":
    mdivision()
    mstrcoding()
