##报警机制
[TOC]

说明

利用周同期数据的统计进行预警：

- 周同期连续下降天数
- 昨日周同期最大跌幅（同比）
- 昨日最大跌幅（环比）【这个部分待添加】
- 连续七天周同期跌幅和超出阈值（且最近三天连续下跌）
- 滑动平均/多项式拟合等算法等的预测值和真实值的差距范围超出预期【待实现】
  - 这个部分需要使用到统计学和机器学习的知识点，看自己能做出什么样的成果吧

 ##参考