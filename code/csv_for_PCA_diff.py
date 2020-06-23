# -*- coding: utf-8 -*-
"""
標準化に微分を使ったバージョン
"""


import os
os.chdir(os.path.abspath(r"D:/GitHub/chemometrics/code"))
import numpy as np
import pandas as pd

source_dir = os.path.abspath(r"D:/テレワーク/データ/kasamatsu_source")
output_dir = os.path.abspath(r"D:/テレワーク/データ/kasamatsu_output")

#"deg"と"pyro"で指定
sample_type = "deg"
#sample_type = "pyro"
output_name = sample_type + r"_all_no_normalized.csv"
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
    
    normalized_intensity = [0]
    normalized_intensity.extend(np.diff(intensity, n=1).tolist())
    df_all.loc[filename] = normalized_intensity
    #標準化しないときは下の一文をコメントアウト
    df_all.loc[filename] = intensity
    df_all = df_all.rename(index = {filename : title})
    

df_all.to_csv(os.path.join(output_dir, output_name))

"""
Created on Wed Jun 17 09:49:08 2020

@author: hfta_
"""

