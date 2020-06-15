# -*- coding: utf-8 -*-
"""
とりあえずPCA
"""
import os, re
os.chdir(os.path.abspath(r"D:/GitHub/chemometrics/code"))
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn.decomposition import PCA

source_dir = os.path.abspath(r"C:/Users/Chem3-MT/Documents/04.プログラミング/Python/油類鑑定/AIA/kasamatsu")
output_dir = os.path.abspath(r"C:/Users/Chem3-MT/Documents/04.プログラミング/Python/油類鑑定/AIA/kasamatsu")

target = "deg_all.csv"
figname = target.split(".")[0] + r".png"
csv_dir = os.path.join(source_dir, target)
#ファイルの読み込み
df = pd.read_csv(csv_dir, sep=",", index_col=0)

#PCAの実行
pca = PCA()
pca.fit(df)
#データを主成分空間に写像
feature = pca.transform(df)

#プロット
regex = re.compile("\d+")
plt.figure(figsize=(6, 6))
plt.scatter(feature[:, 0], feature[:, 1], alpha=0.8, c=list(df.iloc[:, 0]))
for x, y, name in zip (feature[:, 0], feature[:, 1], df.index):
    label = regex.findall(name)
    plt.text(x, y, label[0])
plt.grid()
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.savefig(os.path.join(output_dir,figname), dpi = 400, bbox_inches = "tight")
plt.show()


"""
Created on Mon Jun 15 15:37:17 2020

@author: Chem3-MT
"""

