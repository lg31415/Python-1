#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Fun:tensorflow softmax模型训练和识别
    Ref:
    Date:2016/9/18
    Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf


class TensorOCR(object):
    def __init__(self,train_samples,train_labels):
        self.trainsamples=train_samples
        self.train_labels=train_labels
        self.x = tf.placeholder(tf.float32, [None, 784])
        self.W = tf.Variable(tf.zeros([784,10]))
        self.b = tf.Variable(tf.zeros([10]))
        self.y = tf.nn.softmax(tf.matmul(self.x,self.W) + self.b)   #softmax模型的预测的y值
        self.y_ = tf.placeholder("float", [None,10]) #真实的y值

    def train(self):
        # 模型训练
        cross_entropy = -tf.reduce_sum(self.y_*tf.log(self.y))
        train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

        init = tf.initialize_all_variables()
        sess = tf.InteractiveSession()
        sess.run(init)
        sess.run(train_step, feed_dict={self.x: self.train_samples, self.y_: self.train_labels})  # 真正开始训练(模型能保存吗？)

    def test(self,test_samples,test_labels):
        self.train()
        correct_prediction = tf.equal(tf.argmax(self.y, 1), tf.argmax(self.y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))  #只是一个处理节点
        print(accuracy.eval({self.x: test_samples, self.y_: test_labels})) # 准确率


'''
    获取数据
'''
def loaddata():
    flags = tf.app.flags
    FLAGS = flags.FLAGS
    flags.DEFINE_string('data_dir', './data', 'Directory for storing data')
    mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True) # 获取训练和测试和验证数据集

'''
    tensorflow softmax模型训练和测试
'''
def tensorocr(train_samples,train_labels,test_samples,test_labels):
    # 模型训练
    x = tf.placeholder(tf.float32, [None, 784])
    W = tf.Variable(tf.zeros([784,10]))
    b = tf.Variable(tf.zeros([10]))

    y = tf.nn.softmax(tf.matmul(x,W) + b)   #softmax模型的预测的y值
    y_ = tf.placeholder("float", [None,10]) #真实的y值

    cross_entropy = -tf.reduce_sum(y_*tf.log(y))
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

    init = tf.initialize_all_variables()
    sess = tf.InteractiveSession()
    sess.run(init)
    sess.run(train_step, feed_dict={x: train_samples, y_: train_labels})  # 真正开始训练(模型能保存吗？)

    # 模型测试
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1)) # tf.argmax(y, 1)预测值
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))  #只是一个处理节点
    print(accuracy.eval({x: test_samples, y_: test_labels})) # 准确率


if __name__ == "__main__":
    # 对象式
    tensorocr=TensorOCR()
    # 函数式
    tensorocr()

