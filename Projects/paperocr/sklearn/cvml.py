#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:利用opencv自带的机器学习库进行学习
	Ref:
	Date:2016/9/17
	Author:tuling56
'''
import os
import sys
import re
import cv2
import  numpy as np

reload(sys)
sys.setdefaultencoding('utf-8')

'''
	数据准备
'''
from sklearn import cross_validation # 用于训练和测试分开
from sklearn import preprocessing    # 预处理
def loaddata():
	X=np.loadtxt('./data/samples',dtype=np.float32,delimiter=',')
	# data normalization
	norm_X=preprocessing.normalize(X)
	stand_X=preprocessing.scale(X)
	y=np.loadtxt('./data/labels_c', dtype=np.float32,converters={ 0 : lambda ch : ord(ch)-ord('A')})
	#随机抽取生成训练集和测试集，其中训练集的比例为60%，测试集40%
	X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.4, random_state=0)
	return  X_train, X_test, y_train, y_test

'''
	分类算法
'''
class StatModel(object):
    def load(self, fn):
        self.model.load(fn)
    def save(self, fn):
        self.model.save(fn)

class SVM(StatModel):
    def __init__(self, C = 1, gamma = 0.5):
        self.params = dict( kernel_type = cv2.SVM_RBF,
                            svm_type = cv2.SVM_C_SVC,
                            C = C,
                            gamma = gamma )
        self.model = cv2.SVM()

    def train(self, samples, responses):
        self.model = cv2.SVM()
        self.model.train(samples, responses, params = self.params)

    def predict(self, samples):
        return self.model.predict_all(samples).ravel()

'''
    KNN
'''
class KNearest(StatModel):
    def __init__(self, k = 3):
        self.k = k
        self.model = cv2.KNearest()

    def train(self, samples, responses):
        self.model = cv2.KNearest()
        self.model.train(samples, responses)

    def predict(self, samples):
        retval, results, neigh_resp, dists = self.model.find_nearest(samples, self.k)
        return results.ravel()

from sklearn import metrics
if __name__ == "__main__":
    X_train, X_test, y_train, y_test=loaddata()

    print 'training SVM...'
    #model = SVM(C=2.67, gamma=5.383)
    model = KNearest(k=4)
    model.train(X_train, y_train)
    print 'saving SVM as "digits_svm.dat"...'
    #model.save('letter_svm.dat')

    print 'testing SVM...'
    train_rate = np.mean(model.predict(X_train) == y_train)
    test_rate  = np.mean(model.predict(X_test) == y_test)
    print 'train rate: %f  test rate: %f' % (train_rate*100, test_rate*100)

    # 生成混淆矩阵(对误判情况进行分析：行代表实际，列代表预测)
    print metrics.confusion_matrix(y_test, model.predict(X_test))

