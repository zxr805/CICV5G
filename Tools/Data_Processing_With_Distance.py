###############################################################################
# Copyright (c) 2024 Tongji University
#
# This file is part of 5G V2N2V Dataset.
#
# Created on: 2024/08/20
# Author: Junpeng Huang
#
# Description:
# This code focuses on processing the data, calculating the distance traveled for each point and adding it to the same column
###############################################################################


import numpy as np
import pandas as pd

df1 = pd.read_csv('ego_info_single.txt', sep='\s+', header=0)


distances = [0]
utmX = df1['utmX(m)'].values
utmY = df1['utmY(m)'].values

for i in range(1, len(df1)):
    dist = np.sqrt((utmX[i] - utmX[i - 1]) ** 2 + (utmY[i] - utmY[i - 1]) ** 2)
    distances.append(distances[-1] + dist)

df1['distance'] = distances

df1.to_csv('ego_info_single_distance.txt', sep=' ', index=False)