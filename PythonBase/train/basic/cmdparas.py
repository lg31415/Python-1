#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:命令行参数解析
	Ref:http://www.tuicool.com/articles/jaqQvq
	Date:2016/9/18
	Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

import  getopt
from optparse import OptionParser

def fun():
    pass

# 利用getopt实现参数解析
if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], '', ['model=', 'data=', 'load=', 'save='])
    print "opts:",opts,"\nargs:",args
    for i in sys.argv:
        print(i)

# 利用OptionParser实现参数解析
if __name__=="__main__":
    op = OptionParser(usage="%prog [options]")
    op.add_option("-s", "--status", action="store_true", help="")
    op.add_option("-r", "--reset",  action="store_true", help="")
    op.add_option("-l", "--learn",  metavar="dataset count_spam count_ham", type="string", nargs=3, help="")
    op.add_option("-t", "--test", metavar="dataset threshold", type="string", nargs=2, help="")
    op.add_option("-i", "--tfidf", metavar="dataset", type="string", help="")
    op.add_option("-x", "--chi", metavar="dataset", type="string", help="")

    options, args = op.parse_args()
    # print options

    t = Test()

    if options.status:
        t.status()
    elif options.reset:
        t.reset()
    elif options.learn:
        t.learn(options.learn[0], options.learn[1], options.learn[2])
    elif options.test:
        print options.test
        t.test(options.test[0], options.test[1])
    elif options.tfidf:
        t.tfidf(options.tfidf)
    elif options.chi:
        t.chi(options.chi)
    else:
        print "wrong happen"
