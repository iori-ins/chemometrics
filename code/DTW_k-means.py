# -*- coding: utf-8 -*-
"""
Dynamic Time Wraping k-means clustering
動的時間伸縮法を使ったk-meansをやる
"""
import os, re
os.chdir(os.path.abspath(r"D:/GitHub/chemometrics/code"))
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tslearn.clustering import KShape
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from sklearn.decomposition import PCA

source_dir = os.path.abspath(r"D:/テレワーク/データ/kasamatsu_output")
output_dir = os.path.abspath(r"D:/テレワーク/データ/kasamatsu_output")

target = "deg_all_no_normalized.csv"
figname = target.split(".")[0] + r"_k-shape_c.png"
fig_dir = os.path.join(output_dir, figname)
csv_dir = os.path.join(source_dir, target)

#ファイルの読み込みと前処理
regex = re.compile("\d+")
label_list = []
df = pd.read_csv(csv_dir, sep=",", index_col=0)
stack_list =[]
for index in df.index:
    value = [[i] for i in df.loc[index].tolist()]
    stack_list.append(value)
    label_list.append(int(regex.findall(index)[0]))
stack_data = np.stack(stack_list, axis=0)

#正規化処理
seed = 0
np.random.seed(seed)
stack_data = TimeSeriesScalerMeanVariance(mu=0.0, std=1.0).fit_transform(stack_data)

#KShapeクラスのインスタンス化
ks = KShape(n_clusters=9, n_init=10, verbose=True, random_state=seed)
y_pred = ks.fit_predict(stack_data)

#クラスタリングが成功しているか確認
class_list = []
for i in range(9):
    class_list.append([])
pair = zip(label_list, y_pred)
for i, j in pair:
    class_list[j].append(i)
color_palette = ["black", "dimgrey", "cyan", "gold", "blue", "sienna", "seagreen", "red", "purple"]
color_list=[]
for c in class_list:
    color_list.extend(c)

#クラスタリングして可視化
fig = plt.figure()
plt.figure(figsize=(16,24))
count=0
for yi in range(9):
    plt.subplot(9, 1, 1 + yi)
    for xx in stack_data[y_pred == yi]:
        plt.plot(xx.ravel(), "k-", alpha=.6, color = color_palette[color_list[count]-1], lw=0.5)
        count+=1
    #plt.plot(ks.cluster_centers_[yi].ravel(), "r-")
    plt.title("Cluster {}".format(str(class_list[yi])))
    
plt.tight_layout()
plt.savefig(fig_dir)
plt.show()


"""
Created on Wed Jun 17 11:44:29 2020

@author: hfta_
"""

