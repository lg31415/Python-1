#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Fun:cnn进行手写数字识别
	Ref:http://www.jeyzhang.com/tensorflow-learning-notes-2.html
	Date:2016/9/19
	Author:tuling56
'''
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

def weight_varible(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


'''
    训练和识别部分
'''
flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('data_dir', './data', 'Directory for storing data')
flags.DEFINE_string('model_dir', './data/model', 'Directory for storing data')

mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True) # 获取训练和测试和验证数据集
print("Download Done!")

def cnn_handigit():
    sess = tf.InteractiveSession()

    # paras
    W_conv1 = weight_varible([5, 5, 1, 32])
    b_conv1 = bias_variable([32])

    # conv layer-1
    x = tf.placeholder(tf.float32, [None, 784])
    x_image = tf.reshape(x, [-1, 28, 28, 1])

    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    # conv layer-2
    W_conv2 = weight_varible([5, 5, 32, 64])
    b_conv2 = bias_variable([64])

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    # full connection
    W_fc1 = weight_varible([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    # dropout
    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # output layer: softmax
    W_fc2 = weight_varible([1024, 10])
    b_fc2 = bias_variable([10])

    y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
    y_ = tf.placeholder(tf.float32, [None, 10])

    # model training
    cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    correct_prediction = tf.equal(tf.arg_max(y_conv, 1), tf.arg_max(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    sess.run(tf.initialize_all_variables())

    saver = tf.train.Saver()
    tf.add_to_collection('train_op', train_step)
    for i in range(200):
        batch = mnist.train.next_batch(50)
        if i % 100 == 0:
            train_accuacy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
            print("step %d, training accuracy %g"%(i, train_accuacy))
            saver.save(sess,'train_process',global_step=i)  #在保存的时候
        train_step.run(feed_dict = {x: batch[0], y_: batch[1], keep_prob: 0.5})

    # accuacy on test
    print("test accuracy %g"%(accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0})))

'''
    模型加载测试
'''
def loadtest():
    saver=tf.train.Saver()
    with tf.Session() as persisted_sess:
        new_saver = tf.train.import_meta_graph(FLAGS.model_dir,'train_process.meta')
        print("load model")
        saver.restore(persisted_sess,FLAGS.model_dir,'train_process')
        print("map variables")
        train_step = tf.get_collection('train_op')[0]  #操作op

        #继续训练
        for i in range(200):
            batch = mnist.train.next_batch(50)
            if i % 100 == 0:
               train_step.run(feed_dict = {x: batch[0], y_: batch[1], keep_prob: 0.5})  #这些变量如何恢复



if __name__ == "__main__":
    cnn_handigit()
    loadtest()

