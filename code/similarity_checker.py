# -*- coding: utf-8 -*-
"""
類似度判別プログラム
"""
import os, csv, copy, datetime
os.chdir(os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA"))
import numpy as np
import pandas as pd

#TODO:ディレクトリの整備
sim_dir = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\similarity")
ref_dir = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\similarity\refference")
sample_dir = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\similarity\sample")

#TODO:抽出するイオンとカットオフラインの設定
target_ion = [0, 57, 83, 91, 105, 119, 117, 131, 142, 156]     #0はTIC
cut_off = 0.05                                                 #トップピークに対する比率
mz_range = 0.3                                                 #フラグメントイオンの範囲
lower_limit = 34.0

#TODO:コサイン類似度の関数定義
def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

#TODO:標品から値を抜き出す
ref = []
ref_number = 0
ref_names =[]
for filename in os.listdir(sample_dir):
    if not filename.startswith(("WG", "WK")) or not filename.endswith(("N1.csv", "N2.csv")):
        continue
    ref_data = pd.read_csv(os.path.join(ref_dir, filename), header = 0, index_col = 0)
    rt = [float(i) for i in list(ref_data.columns)]
    print("標品　　{}を読み込み中...".format(filename))
    box = [filename]
    for i in target_ion:
        box.append([i])
    ref.append(box)
#TODO:標品の抽出イオンプロファイルをリストに格納する   
    for ion in target_ion:
        if ion == 0:
            intensity = np.array(ref_data.loc["total_intensity"])
            title = r"{} TIC".format(filename.split(".")[0])
        else:
            number = (ion - lower_limit)*10 + ref_data.index.get_loc(str(lower_limit))           #locでは1024行目以降が読めない
            intensity = np.array(ref_data.iloc[int(number - mz_range*10) : int(number + mz_range*10)])
            title = r"{} m/z = {}".format(filename.split(".")[0], ion)
            for i in range(1, len(intensity)):
                intensity[0] += intensity[i]
            intensity = intensity[0]
        max_intensity = int(max(intensity))
        intensity = (intensity*100)/max_intensity
        offset = target_ion.index(ion) + 1
        ref[ref_number][offset].extend(np.array(intensity))
    ref_number += 1
    ref_names.append([filename.split(".")[0]])
    
#TODO:CSVファイルを開きヘッダーを書き込む
now = datetime.datetime.now()
title = 'similarity_c_{0:%Y%m%d%H}.csv'.format(now)
csv_file_obj = open(os.path.join(sim_dir, title), "w", newline = "", encoding = "utf-8")
writer = csv.writer(csv_file_obj)
header = ["filename", "most similar"]
header.extend(target_ion)
writer.writerow(header)
    
#TODO:ファイルを抜き出してループ
for filename in os.listdir(sample_dir):
    if filename.startswith("W") and not filename.endswith(("N1.csv", "N2.csv")):
        filetype = "other"
        continue
    if filename.startswith(("G", "WG")):
        filetype = "gasoline"
    elif filename.startswith(("K", "WK")):
        filetype = "kerosene"
    else:                   #ガソリン灯油に関係ないファイルは飛ばす
        filetype = "other"
        continue
    data = pd.read_csv(os.path.join(sample_dir, filename), header = 0, index_col = 0)
    rt = [float(i) for i in list(data.columns)]
    print("サンプル{}を読み込み中...".format(filename))
    filedata =[]
    filedata.append(filename.split(".")[0])
    ion_sim = [filename.split(".")[0]]
    similarity = []
    similarity.extend(copy.deepcopy(ref_names))
#TODO:指定されたフラグメントイオンだけループする
    for ion in target_ion:
        if ion == 0:
            intensity = np.array(data.loc["total_intensity"])
        else:
            number = (ion - lower_limit)*10 + data.index.get_loc(str(lower_limit))           #locでは1024行目以降が読めない
            intensity = np.array(data.iloc[int(number - mz_range*10) : int(number + mz_range*10)])
            for i in range(1, len(intensity)):
                intensity[0] += intensity[i]
            intensity = intensity[0]
#TODO:強度の規格化            
        max_intensity = max(intensity)
        if max_intensity <1:
            max_intensity =1
        intensity = np.array(intensity*100/max(intensity))
            
#TODO:各標品との類似度の計算
        ion_index = target_ion.index(ion) + 1
        for r in range(len(ref)):
            similarity[r].append(round(cos_sim(intensity, ref[r][ion_index][1:]), 2))

#TODO:類似度の高い標品を計算し、CSVに記述する
    highest = 0
    h_index = 0
    for i in range(len(similarity)):
        sim_sum = sum(similarity[i][1:])
        if sim_sum > highest:
            highest = sim_sum
            h_index = i
    ion_sim.extend(copy.copy(similarity[h_index]))
    writer.writerow(ion_sim)
    ion_sim.clear()
    
    
csv_file_obj.close()
            


#TODO:クロマトグラムの保存



"""
Created on Mon Mar 23 15:25:36 2020

@author: Chem3-MT
"""

