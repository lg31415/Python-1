#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:random模块学习
    Ref:https://docs.python.org/3.5/library/random.html#module-random
    Date:2016/9/2
    Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

import random
def mrandom():
    print random.random()                      # Random float x, 0.0 <= x < 1.0
    print random.uniform(1, 10)                # Random float x, 1.0 <= x < 10.0   #等同于 np.floor(10*random.random())
    print random.randrange(10)                 # Integer from 0 to 9
    print random.randrange(0, 101, 2)          # Even integer from 0 to 100
    print random.choice('abcdefghij')          # Single random element
    items = [1, 2, 3, 4, 5, 6, 7]
    random.shuffle(items)                        #in_place操作
    print items
    print random.sample([1, 2, 3, 4, 5],  3)   # Three samples without replacement


if __name__ == "__main__":
    mrandom()

