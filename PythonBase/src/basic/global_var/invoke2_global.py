#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Date:
    Author:tuling56
'''
import os
import sys
#print sys.getdefaultencoding()
#reload(sys)
#sys.setdefaultencoding('utf-8')

import global_var as G
import invoke_global as V1

def run():
    G.g_maillist.append('this is append')
    print G.g_maillist



if __name__ == "__main__":
    print "invoke 1"
    run()
    V1.run()

