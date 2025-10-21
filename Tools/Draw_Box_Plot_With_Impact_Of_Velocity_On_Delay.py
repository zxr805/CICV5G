# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c) 2024 Tongji University
#
# This file is part of 5G V2N2V Dataset.
#
# Created on: 2024/08/20
# Author: Egik Von
#
# Description:
# This code focuses on impact of velocity on 5G V2N2V delay,draw the box-plot
###############################################################################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('', delimiter='\s+')
data1 = pd.read_csv('', delimiter='\s+')
data2 = pd.read_csv('', delimiter='\s+')
data3 = pd.read_csv('', delimiter='\s+')
data4 = pd.read_csv('', delimiter='\s+')
data5 = pd.read_csv('', delimiter='\s+')
data6 = pd.read_csv('', delimiter='\s+')
data7 = pd.read_csv('', delimiter='\s+')

delay = data['delay(ms)']
delay1 = data1['delay(ms)']
delay2 = data2['delay(ms)']
delay3 = data3['delay(ms)']
delay4 = data4['delay(ms)']
delay5 = data5['delay(ms)']
delay6 = data6['delay(ms)']
delay7 = data7['delay(ms)']

mean_delay = np.mean(delay)
variance_delay = np.std(delay)
mean_delay1 = np.mean(delay1)
variance_delay1 = np.std(delay1)
mean_delay2 = np.mean(delay2)
variance_delay2 = np.std(delay2)
mean_delay3 = np.mean(delay3)
variance_delay3 = np.std(delay3)
mean_delay4 = np.mean(delay4)
variance_delay4 = np.std(delay4)
mean_delay5 = np.mean(delay5)
variance_delay5 = np.std(delay5)
mean_delay6 = np.mean(delay6)
variance_delay6 = np.std(delay6)
mean_delay7 = np.mean(delay7)
variance_delay7 = np.std(delay7)

data_all1 = {'0': delay4,'20': delay5,'30': delay6,'40': delay7}
data_all2 = {'50': delay,'60': delay1,'70': delay2,'80': delay3}
df1 = pd.DataFrame(data_all1)
df2 = pd.DataFrame(data_all2)

plt.figure(figsize=(9, 6))

f1 = df1.boxplot(sym='w.', patch_artist=True, return_type='dict', meanline=False, showmeans=False)

for box in f1['boxes']:
    box.set(color='blue', linewidth=2)
    box.set(facecolor='white')
for whisker in f1['whiskers']:
    whisker.set(color='blue', linewidth=2)
for cap in f1['caps']:
    cap.set(color='blue', linewidth=2)
for median in f1['medians']:
    median.set(color='blue', linewidth=2)
for mean in f1['means']:
    mean.set(color='red')


positions = np.array(range(1, 5))

f2 = df2.boxplot(sym='w.', patch_artist=True, positions=positions + 4,return_type='dict', meanline=False, showmeans=False)

for box in f2['boxes']:
    box.set(color='black', linewidth=2)
    box.set(facecolor='white')
for whisker in f2['whiskers']:
    whisker.set(color='black', linewidth=2)
for cap in f2['caps']:
    cap.set(color='black', linewidth=2)
for median in f2['medians']:
    median.set(color='black', linewidth=2)
for mean in f2['means']:
    mean.set(color='red')

mean_values1 = [mean_delay4,mean_delay5,mean_delay6,mean_delay7]
mean_values2 = [mean_delay,mean_delay1,mean_delay2,mean_delay3]
mean_values=mean_values1+mean_values2

positions = np.concatenate([np.arange(1, 5), np.arange(1, 5) + 4])

plt.plot(positions, mean_values, marker='o', markerfacecolor='blue', markeredgecolor='blue', color='r', linestyle='-', linewidth=3)

df=df1+df2
plt.xticks(positions, list(df1.columns) + list(df2.columns), fontsize=14)
plt.yticks( fontsize=14)

plt.grid(False)
plt.savefig("",dpi=900)
plt.show()

