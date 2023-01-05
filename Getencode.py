#!/usr/bin/env python
# coding: utf-8
import numpy as np
import csv


def getencoding():
    classNames = []  # 裝載名字
    encodeList = []  # 裝載每個人的特徵
    with open('csvfile/facecode.csv', mode ='r+', newline='', encoding ="utf-8") as f:  # read and write mode in same time
        reader = csv.reader(f)
        headers = next(reader)  # 跳過第一列 (欄位顯示)
        for row in reader:
            classNames.append(row[0])  # row[0] 為 name
            encodeList.append(np.array(eval(row[1])))  # row[1] 為 encoding , eval: 把字串裡面的內容取出來並成為數值 (有點像format的相反)
    return classNames, encodeList

if __name__ == '__main__': 
    getencoding()




