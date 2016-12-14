#!/usr/bin/env python
# -*- coding: utf8 -*-
__author__ = 'yjm'
'''
  功能注释：base64编解码
'''

import base64

def mbase64():
    s='base64编码技术'
    se=base64.b64encode(s)
    de=base64.b64decode(se)
    print s,se,de


if __name__ == "__main__":
    mbase64()
