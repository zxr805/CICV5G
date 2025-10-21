###############################################################################
# Copyright (c) 2024 Tongji University
#
# This file is part of 5G V2N2V Dataset.
#
# Created on: 2024/08/12
# Author: Junpeng Huang
#
# Description:
# This code mainly reads text data and counts the number of times rsrp occurs with different sized delays at different ranges and outputs it to an xlsx file.
###############################################################################


date1= []
date2= []
date3= []
with open('v2v_info01.txt','r') as f:
    next(f)
    for line in f:
        date1.append(line.strip().split())
with open('v2v_info02.txt','r') as f:
    next(f)
    for line in f:
        date2.append(line.strip().split())
with open('v2v_info03.txt','r') as f:
    next(f)
    for line in f:
        date3.append(line.strip().split())

rsrp_ranges = {"-75": [0, 0, 0], "-85": [0, 0, 0], "-90": [0, 0, 0], "-95": [0, 0, 0], "<-95": [0, 0, 0]}
total_count = 0


for data in [date1, date2, date3]:
    for line in data:
        rsrp = float(line[9])
        delay = float(line[2])
        total_count += 1


        if rsrp > -75:
            rsrp_ranges["-75"][2] += 1
            if delay > 100:
                rsrp_ranges["-75"][0] += 1
            elif 50 <= delay <= 100:
                rsrp_ranges["-75"][1] += 1
        elif rsrp > -85:
            rsrp_ranges["-85"][2] += 1
            if delay > 100:
                rsrp_ranges["-85"][0] += 1
            elif 50 <= delay <= 100:
                rsrp_ranges["-85"][1] += 1
        elif rsrp > -90:
            rsrp_ranges["-90"][2] += 1
            if delay > 100:
                rsrp_ranges["-90"][0] += 1
            elif 50 <= delay <= 100:
                rsrp_ranges["-90"][1] += 1
        elif rsrp > -95:
            rsrp_ranges["-95"][2] += 1
            if delay > 100:
                rsrp_ranges["-95"][0] += 1
            elif 50 <= delay <= 100:
                rsrp_ranges["-95"][1] += 1
        else:
            rsrp_ranges["<-95"][2] += 1
            if delay > 100:
                rsrp_ranges["<-95"][0] += 1
            elif 50 <= delay <= 100:
                rsrp_ranges["<-95"][1] += 1


for key, value in rsrp_ranges.items():
    print(f"For rsrp > {key}, delay > 100: {value[0]}, 50 <= delay <= 100: {value[1]}, total rsrp count: {value[2]}")
print("total:",total_count)

for key, value in rsrp_ranges.items():
    percent_1 = (value[0] / total_count) * 100
    percent_2 = (value[1] / total_count) * 100
    print(f"For rsrp > {key}, delay > 100: {percent_1}%, 50 <= delay <= 100: {percent_2}%")

for key, value in rsrp_ranges.items():
    print(f"For rsrp > {key}, delay > 100: {value[0]}, 50 <= delay <= 100: {value[1]}")

import xlsxwriter
workbook = xlsxwriter.Workbook('rsrp_delay.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'rsrp')
worksheet.write('B1', 'delay > 100')
worksheet.write('C1', '50 <= delay <= 100')
worksheet.write('D1', 'total rsrp count')
worksheet.write('E1', 'percent delay > 100')
worksheet.write('F1', 'percent 50 <= delay <= 100')
worksheet.write('G1', 'total count')
row = 1
for key, value in rsrp_ranges.items():
    worksheet.write(row, 0, key)
    worksheet.write(row, 1, value[0])
    worksheet.write(row, 2, value[1])
    worksheet.write(row, 3, value[2])

    percent_1 = (value[0] / total_count) * 100
    percent_2 = (value[1] / total_count) * 100
    worksheet.write(row, 4, percent_1)
    worksheet.write(row, 5, percent_2)

    worksheet.write(row, 6, total_count)

    row += 1

workbook.close()