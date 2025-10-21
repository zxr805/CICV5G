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
# This code focuses on impact of communication delay on position deviation at a speed of 30 km/h.including RSRP Delay and Distance
###############################################################################
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']

data = pd.read_csv('', delimiter='\s+')
utmx=data["utmX(m)"]
utmy=data["utmY(m)"]
currentx=data["currentX(m)"]
currenty=data["currentY(m)"]
distance_diff = np.sqrt((utmx - currentx)**2 + (utmy - currenty)**2)

subtime=(data["sub_time(ms)"]-data["sub_time(ms)"][0])/1000
delay=data["delay(ms)"]
rsrp=data["rsrp(db)"]

fig, axs = plt.subplots(3, 1, figsize=(12, 8))

axs[0].scatter(subtime, rsrp,color='#2C91E0', label="RSRP",marker='.')
axs[0].tick_params(axis='both', labelsize=13)
axs[0].set_xticks([])
axs[0].set_ylabel('RSRP (dBm)', fontsize=15, labelpad=7)
axs[0].set_yticks(range(-100, -60, 5))

axs[1].plot(subtime, delay,color='#3ABF99', linewidth=1, label="delay",marker='o',markersize=3)
axs[1].tick_params(axis='both', labelsize=13)
axs[1].set_xticks([])
axs[1].set_ylabel('Delay (ms)', fontsize=15, labelpad=17)


axs[2].plot(subtime, distance_diff,color='#F0A73A', linewidth=1,label="distance" ,marker='*',markersize=3)
axs[2].tick_params(axis='both', labelsize=13)
axs[2].set_xlabel('Time (s)', fontsize=15)
axs[2].set_ylabel('Distance (m)', fontsize=15, labelpad=28)

plt.savefig("",dpi=900)

plt.show()
