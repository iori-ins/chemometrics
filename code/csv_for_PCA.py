# -*- coding: utf-8 -*-
"""
PCA用データ前処理プログラム
保持時間と強度だけにする
分析対象のファイルを全部書き込む
"""

import os
os.chdir(os.path.abspath(r"D:/GitHub/chemometrics/code"))
import csv
import numpy as np
import pandas as pd

source_dir = os.path.abspath(r"C:/Users/Chem3-MT/Documents/04.プログラミング/Python/油類鑑定/AIA/kasamatsu_csv")
output_dir = os.path.abspath(r"C:/Users/Chem3-MT/Documents/04.プログラミング/Python/油類鑑定/AIA/kasamatsu")

#"deg"と"pyro"で指定
sample_type = "deg"
#sample_type = "pyro"
filename = sample_type + r"_all.csv"
sample_type += r".csv"

filelist = []
for csv in os.listdir(source_dir):
    if csv.startswith("blank") or not csv.endswith(sample_type):
        continue
    else:
        filelist.append(csv)

first = True
for csv in filelist:
    csv_dir = os.path.join(source_dir, csv)
    title = csv.split(".")[0]
    df = pd.read_csv(csv_dir, sep=",", index_col=None)
    print("{}を処理中……".format(csv))
    if first:
        rt = df.columns[1:].tolist()
        df_all = pd.DataFrame(np.zeros_like, columns = rt, index = filelist)
        first = False
    intensity = df.iloc[0][1:].tolist()
    normalized_intensity = []
    for i in intensity:
        normalized_intensity.append(i*1000/sum(intensity))
    df_all.loc[csv] = normalized_intensity
    df_all = df_all.rename(index = {csv : title})

df_all.to_csv(os.path.join(output_dir, filename))


"""
Created on Mon Jun 15 11:26:53 2020

@author: Chem3-MT
"""

