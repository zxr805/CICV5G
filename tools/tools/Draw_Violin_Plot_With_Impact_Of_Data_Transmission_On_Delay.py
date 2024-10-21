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
# This code focuses on impact of data transmission frequency on 5G V2N2V delay,draw the violin-plot
###############################################################################
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('', delimiter='\s+')
data1 = pd.read_csv('', delimiter='\s+')
data2 = pd.read_csv('', delimiter='\s+')
data3 = pd.read_csv('', delimiter='\s+')
data4 = pd.read_csv('', delimiter='\s+')
data5 = pd.read_csv('', delimiter='\s+')
data6 = pd.read_csv('', delimiter='\s+')
data7 = pd.read_csv('', delimiter='\s+')

sns.violinplot(x=10, y='delay(ms)', data=data,color='#397FC7')#,bw=0.0)
sns.violinplot(x=20, y='delay(ms)', data=data1,color='#397FC7')#,bw=0.0)
sns.violinplot(x=33, y='delay(ms)', data=data2,color='#397FC7')#,bw=0.0)
sns.violinplot(x=100, y='delay(ms)', data=data3,color='#397FC7')#,bw=0.0)

plt.savefig("",dpi=900)
plt.show()
