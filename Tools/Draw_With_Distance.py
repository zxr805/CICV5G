###############################################################################
# Copyright (c) 2024 Tongji University
#
# This file is part of 5G V2N2V Dataset.
#
# Created on: 2024/08/20
# Author: Junpeng Huang
#
# Description:
# This code mainly plots the curvature change, lateral deviation change, heading deviation change, and speed change of the autopilot's actual driving route from the reference line
###############################################################################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors


def caculate_distance(df1, df2):
    Deviation = []
    Position = []
    points_df1 = df1[['utmX(m)', 'utmY(m)']].values
    nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(points_df1)

    for i in range(len(df2)):
        point = df2.iloc[i][['utmX(m)', 'utmY(m)']].values
        distances, indices = nbrs.kneighbors([point])
        point_b = points_df1[indices[0][0]]
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

        heading = df1.iloc[indices[0][0]]['heading(rad)']
        dx =point[0] - point_b[0]
        dy = point[1] - point_b[1]

        x = dx * (-np.sin(heading)) + dy * np.cos(heading)
        if x > 0:
            h = -h
        Deviation.append(h)

    return Deviation


def caculate_heading(df1, df2):
    points_df1 = df1[['utmX(m)', 'utmY(m)']].values
    points_df2 = df2[['utmX(m)', 'utmY(m)']].values

    distances = np.linalg.norm(points_df1[:, None] - points_df2, axis=2)

    indices = np.argmin(distances, axis=0)

    heading_deviation = df1.iloc[indices]['heading(rad)'].values - df2['heading(rad)']

    return heading_deviation.tolist()

def caculate_curvature(x1,y1,x2,y2,x3,y3):

    x_m1 = (x1 + x2) / 2
    y_m1 = (y1 + y2) / 2
    x_m2 = (x2 + x3) / 2
    y_m2 = (y2 + y3) / 2

    k1 = (y2 - y1) / (x2 - x1)
    k2 = (y3 - y2) / (x3 - x2)

    k_m1 = -1 / k1
    k_m2 = -1 / k2

    b_m1 = y_m1 - k_m1 * x_m1
    b_m2 = y_m2 - k_m2 * x_m2

    x0 = (b_m2 - b_m1) / (k_m1 - k_m2)
    y0 = k_m1 * x0 + b_m1

    r = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    curvature = 1 / r

    if np.sign((x2 - x1) * (y3 - y2) - (x3 - x2) * (y2 - y1))<0:
        curvature = -curvature

    return curvature



df1 = pd.read_csv('cloud_V15_distance.txt', sep='\s+', header=0)
df2 = pd.read_csv('eastloop0821_1distance.txt', sep='\s+', header=0)

df3 = pd.read_csv('single_15_distance.txt', sep='\s+', header=0)
df4 = pd.read_csv('eastloop0821_2distance.txt', sep='\s+', header=0)

df5 = pd.read_csv('eastloop0821_distance.txt', sep='\s+', header=0)

# 设置字体为微软雅黑
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.figure(figsize=(12, 8))
mask1_df1 = df1.iloc[1900:]['heading(rad)'] < 0
df1.loc[df1.index[1900:][mask1_df1], 'heading(rad)'] += 2 * np.pi
mask2_df1 = df1.iloc[3900:]['heading(rad)'] > 0
mask2_df1 = mask2_df1 & ~mask1_df1.reindex_like(mask2_df1, method='ffill')
df1.loc[df1.index[3900:][mask2_df1], 'heading(rad)'] += 2 * np.pi
mask1_df2 = df2.iloc[1000:]['heading(rad)'] < 0
df2.loc[df2.index[1000:][mask1_df2], 'heading(rad)'] += 2 * np.pi


mask2_df2 = df2.iloc[1300:]['heading(rad)'] > 0

mask2_df2 = mask2_df2 & ~mask1_df2.reindex_like(mask2_df2, method='ffill')
df2.loc[df2.index[1300:][mask2_df2], 'heading(rad)'] += 2 * np.pi


mask1_df3 = df3.iloc[2000:]['heading(rad)'] < 0
df3.loc[df3.index[2000:][mask1_df3], 'heading(rad)'] += 2 * np.pi


mask2_df3 = df3.iloc[4100:]['heading(rad)'] > 0

mask2_df3 = mask2_df3 & ~mask1_df3.reindex_like(mask2_df3, method='ffill')
df3.loc[df3.index[4100:][mask2_df3], 'heading(rad)'] += 2 * np.pi


mask1_df4 = df4.iloc[1000:]['heading(rad)'] < 0
df4.loc[df4.index[1000:][mask1_df4], 'heading(rad)'] += 2 * np.pi


mask2_df4 = df4.iloc[1300:]['heading(rad)'] > 0

mask2_df4 = mask2_df4 & ~mask1_df4.reindex_like(mask2_df4, method='ffill')
df4.loc[df4.index[1300:][mask2_df4], 'heading(rad)'] += 2 * np.pi


plt.subplot(4,1,1)
curvatures = []


for i in range(1, len(df2) - 1):
    x1 = df2.iloc[i - 1]['utmX(m)']
    y1 = df2.iloc[i - 1]['utmY(m)']
    x2 = df2.iloc[i]['utmX(m)']
    y2 = df2.iloc[i]['utmY(m)']
    x3 = df2.iloc[i + 1]['utmX(m)']
    y3 = df2.iloc[i + 1]['utmY(m)']
    curvature = caculate_curvature(x1, y1, x2, y2, x3, y3)
    curvatures.append(curvature)

curvatures = pd.Series(curvatures)
curvatures = curvatures.rolling(window=30, min_periods=1).mean()
curvatures = curvatures.fillna(method='bfill')
curvatures = curvatures.fillna(method='ffill')
curvatures = curvatures.tolist()

df2 = df2.iloc[1:-1]

plt.plot(df2["distance"], curvatures, color="#F0A73A")

plt.xlim(0,1000)
plt.ylim(-0.07,0.08)
plt.xticks([])



plt.subplot(4,1,2)
Deviation1 = caculate_distance(df2,df1)
Deviation2 = caculate_distance(df4,df3)


Deviation1 = pd.Series(Deviation1)
Deviation2 = pd.Series(Deviation2)


Deviation1_filtered = Deviation1[df1['distance'].reset_index(drop=True) > 50]
Deviation2_filtered = Deviation2[df3['distance'].reset_index(drop=True) > 50]

print('Cloud-based-deviation-ey:', max(abs(Deviation1_filtered)), min(abs(Deviation1_filtered)),np.mean(abs(Deviation1_filtered)),np.std(abs(Deviation1_filtered)))
print('Single-vehicle-deviation-ey:', max(abs(Deviation2_filtered)), min(abs(Deviation2_filtered)),np.mean(abs(Deviation2_filtered)),np.std(abs(Deviation2_filtered)))

filtered_distance1 = df1.loc[df1['distance'] > 50, 'distance']
filtered_distance3 = df3.loc[df3['distance'] > 50, 'distance']


plt.plot(df1["distance"], Deviation1, label='CICV', color='#BF1D2D')
plt.plot(df3["distance"], Deviation2, label='AV', color='#397FC7')
plt.legend(loc='upper right', bbox_to_anchor=(1, 1.02),borderpad=0.2)

plt.xlim(0,1000)
plt.xticks([])
plt.ylim(-0.25,0.45)

plt.subplot(4,1,3)
heading_deviation1 = caculate_heading(df1,df2)
heading_deviation2 = caculate_heading(df3,df4)

heading_deviation1 = pd.Series(heading_deviation1)
heading_deviation2 = pd.Series(heading_deviation2)

heading_deviation1_filtered = heading_deviation1[df2['distance'].reset_index(drop=True) > 50]
heading_deviation2_filtered = heading_deviation2[df4['distance'].reset_index(drop=True) > 50]

filtered_distance2 = df2.loc[df2['distance'] > 50, 'distance']
filtered_distance4 = df4.loc[df4['distance'] > 50, 'distance']


print('Cloud-based-deviation-heading:', max(heading_deviation1_filtered), min(heading_deviation1_filtered))
print('Single-vehicle-deviation-heading:', max(heading_deviation2_filtered), min(heading_deviation2_filtered))
plt.plot(df2["distance"],heading_deviation1, label='CICV',color='#BF1D2D')
plt.plot(df4["distance"] ,heading_deviation2, label='AV',color='#397FC7')

plt.xlim(0,1000)
plt.xticks([])


plt.subplot(4,1,4)
plt.plot(df1['distance'], df1['velocity(m/s)'], label='CICV',color='#BF1D2D')
plt.plot(df3['distance'], df3['velocity(m/s)'], label='AV',color='#397FC7')

plt.ylim(0,6)
plt.xlim(0,1000)
plt.savefig('east.png', dpi=900)
plt.show()


