###############################################################################
# Copyright (c) 2024 Tongji University
#
# This file is part of 5G V2N2V Dataset.
#
# Created on: 2024/08/21
# Author: Junpeng Huang
#
# Description:
# This code is mainly used to plot the lateral errors under different delay conditions for CICV as well as under AV.
###############################################################################


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import distance
from sklearn.neighbors import NearestNeighbors


def caculate_distance(df1, df2):
    Deviation = []
    Position = []
    points_df1 = df1[['utmX(m)', 'utmY(m)']].values
    nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(points_df1)

    for i in range(len(df2)):
        point = df2.iloc[i][['utmX(m)', 'utmY(m)']].values
        distances, indices = nbrs.kneighbors([point])
        point_b = points_df1[indices[0][0]]     # 取出最近的一个点,point_b格式为[utmX(m),utmY(m)]
        point_c = points_df1[indices[0][1]]
        a = np.linalg.norm(point_b - point_c)
        if a == 0:
            h = distances[0][0]
            Deviation.append(h)
            Position.append('Coincide')
            continue
        b = distances[0][0]
        c = distances[0][1]
        cos_a = (b ** 2 + c ** 2 - a ** 2) / (2 * b * c)
        sin_a = np.sqrt(1 - cos_a ** 2)
        h = (b * c * sin_a) / a
        # 取出最近点的航向角
        heading = df1.iloc[indices[0][0]]['heading(rad)']
        dx =point[0] - point_b[0]
        dy = point[1] - point_b[1]

        x = dx * (-np.sin(heading)) + dy * np.cos(heading)  #np.cos(heading) + (point_b[1] - point[1]) * np.sin(heading)
        if x < 0:
            h = -h
        Deviation.append(h)

    return Deviation



# 读取文件
df1 = pd.read_csv('ego_info_delay_0.1-0.2.txt', sep='\s+', header=0)
df2 = pd.read_csv('ego_info_delay_0.2-0.4.txt', sep='\s+', header=0)
df3 = pd.read_csv('ego_info_delay_0.5-0.7.txt', sep='\s+', header=0)
df4 = pd.read_csv('westloop1_distance.txt', sep='\s+', header=0)
df5 = pd.read_csv('ego_info_single_distance.txt', sep='\s+', header=0)
# 设置字体为微软雅黑
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.figure(figsize=(10, 3))



# 绘制Cloud-based的偏离轨迹距离
Deviation1 = caculate_distance(df4,df1)
Deviation2 = caculate_distance(df4,df2)
Deviation3 = caculate_distance(df4,df3)
Deviation5 = caculate_distance(df4,df5)

plt.plot(df5['distance'],Deviation5, label='AV',color='#C5272D')
plt.plot(df2['distance'],Deviation2, label='Delay2',linestyle = "--",color='#397FC7')
plt.plot(df1['distance'],Deviation1, label='Delay1', linestyle = "-",color='#397FC7')
plt.plot(df3['distance'],Deviation3, label='Delay3',linestyle = ":",color='#397FC7')
    # C5272D
plt.legend(loc='upper right', ncol=2)
# 不显示坐标
plt.xlim(0,285)
plt.ylim(-0.25,1)
plt.savefig('delay_compare_with_single.png', dpi=900)
plt.show()




