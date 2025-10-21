###############################################################################
# Copyright (c) 2024 Tongji University
#
# This file is part of 5G V2N2V Dataset.
#
# Created on: 2024/08/12
# Author: Junpeng Huang
#
# Description:
#This code mainly reads the xlsx file and plots the probability of occurrence of delays greater than 100ms and delays
# between 50ms and 100ms at different signal strengths with speeds of 30km/h, 40km/h, and 50km/h respectively.
###############################################################################
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


data = {
    'range': ['30       40       50 \nWeak Signal', '30       40       50 \nModerate Signal', '30       40       50 \nStrong Signal'], # 'Weak Signal', 'Moderate Signal', 'Strong Signal'
    'V30-Delay:>100ms': [0.074647887, 0.046973803, 0.000337154],
    'V30-Delay:50~100ms': [0.021126761, 0.01535682, 0.000337154],
    'V40-Delay:>100ms': [0.07793765, 0.071174377, 0],
    'V40-Delay:50~100ms': [0.014388489, 0.015421115, 0.000433839],
    'V50-Delay:>100ms': [0.10971223, 0.091528724, 0.001189414],
    'V50-Delay:50~100ms': [0.025179856, 0.031158715, 0.000297354]
}

df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(10, 6))


x = range(len(df['range']))


ax.bar(x, df['V30-Delay:>100ms'], width=0.1, label='V30-Delay:>100ms',color='#ABC6E4')
ax.bar(x, df['V30-Delay:50~100ms'], width=0.1, bottom=df['V30-Delay:>100ms'], label='V30-Delay:50~100ms',color='#C39398')


ax.bar([p + 0.1 for p in x], df['V40-Delay:>100ms'], width=0.1, label='V40-Delay:>100ms',color='#FCDABA')
ax.bar([p + 0.1 for p in x], df['V40-Delay:50~100ms'], width=0.1, bottom=df['V40-Delay:>100ms'], label='V40-Delay:50~100ms',color='#A7D2BA')

ax.bar([p + 0.2 for p in x], df['V50-Delay:>100ms'], width=0.1, label='V50-Delay:>100ms',color='#D0CADE')
ax.bar([p + 0.2 for p in x], df['V50-Delay:50~100ms'], width=0.1, bottom=df['V50-Delay:>100ms'], label='V50-Delay:50~100ms',color='#E7E6D4')


ax.set_xticks([p + 0.1 for p in x])
ax.set_xticklabels(df['range'])


ax.set_xlabel('RSRP', fontsize=12)
ax.set_ylabel('Probability', fontsize=12)

ax.legend()


ax_inset = fig.add_axes([0.78, 0.4, 0.2, 0.3])  # 右上角位置
ax_inset.bar(0, df['V30-Delay:>100ms'][2], width=0.02, color='#ABC6E4')
ax_inset.bar(0, df['V30-Delay:50~100ms'][2], width=0.02, bottom=df['V30-Delay:>100ms'][2], color='#C39398')
ax_inset.bar(0.1, df['V40-Delay:>100ms'][2], width=0.02, color='#FCDABA')
ax_inset.bar(0.1, df['V40-Delay:50~100ms'][2], width=0.02, bottom=df['V40-Delay:>100ms'][2], color='#A7D2BA')
ax_inset.bar(0.2, df['V50-Delay:>100ms'][2], width=0.02, color='#D0CADE')
ax_inset.bar(0.2, df['V50-Delay:50~100ms'][2], width=0.02, bottom=df['V50-Delay:>100ms'][2], color='#E7E6D4')


ax_inset.set_xticks([0.1])
ax_inset.set_xticklabels(['30                          40                          50 \nStrong Signal'], fontsize=8)
ax_inset.set_ylim(0, 0.002)

plt.tight_layout()
plt.savefig('RSRP_Delay.png', dpi=900)
plt.show()

