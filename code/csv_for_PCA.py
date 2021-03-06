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

source_dir = os.path.abspath(r"D:/テレワーク/データ/kasamatsu_source")
output_dir = os.path.abspath(r"D:/テレワーク/データ/kasamatsu_output")

#"deg"と"pyro"で指定
sample_type = "deg"
sample_type = "pyro"
output_name = sample_type + r"_all_flat5.csv"
sample_type += r".csv"

filelist = []
for filename in os.listdir(source_dir):
    if filename.startswith("blank") or not filename.endswith(sample_type):
        continue
    else:
        filelist.append(filename)

first = True
for filename in filelist:
    csv_dir = os.path.join(source_dir, filename)
    title = filename.split(".")[0]
    df = pd.read_csv(csv_dir, sep=",", index_col=None)
    print("{}を処理中……".format(filename))
    if first:
        rt = df.columns[1:].tolist()
        df_all = pd.DataFrame(np.zeros_like, columns = rt, index = filelist)
        first = False
    intensity = df.iloc[0][1:].tolist()
    normalized_intensity = []
    for i in intensity:
        if i >= max(intensity)/20:
            normalized_intensity.append(i*1000/max(intensity))
        else:
            normalized_intensity.append(0)
    df_all.loc[filename] = normalized_intensity
    df_all = df_all.rename(index = {filename : title})

df_all.to_csv(os.path.join(output_dir, output_name))


"""
Created on Mon Jun 15 11:26:53 2020

@author: Chem3-MT
"""

