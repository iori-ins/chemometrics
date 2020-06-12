# -*- coding: utf-8 -*-
"""
TCC類似度判別プログラム
eulid
"""
import os, csv, datetime
os.chdir(os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA"))
import numpy as np
import pandas as pd

#TODO:条件のチェック
tc_ex = False       #拡張ターゲット化合物はがしようされているか。拡張ならTrue
file_check = True  #分析ファイルの選択 Trueならサンプル、Falseなら標品
blank_sub = False   #TCCファイルが減算されているか。減算されているならTrue

#TODO:ディレクトリの整備
sim_dir     = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\similarity")
tcc_dir     = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\similarity\TCC")

#読み込むファイルの指定
data_from = "TCC"
if tc_ex:
    data_from += "_ex"
if blank_sub:
    data_from += "_sub"
ref = data_from + "_refference"
sample = data_from + "_sample"
ref_dir = os.path.join(tcc_dir, ref)
sample_dir = os.path.join(tcc_dir,sample)

#TODO:規格化定数の指定（特に意味はない）
norm = 1  #規格化定数

#TODO:Euclid類似度の関数定義
def euclid_sim(v1, v2):
    e_distance = np.linalg.norm(v1-v2)
    max_vec = np.full(len(v1), norm)
    min_vec = np.zeros(len(v1))
    max_distance = np.linalg.norm(max_vec-min_vec)
    return (1 - e_distance/max_distance)

#TODO:標品から値を抜き出してデータフレームに格納
g_first = True
k_first = True
g_names = []
k_names = []
for filename in os.listdir(ref_dir):
    if filename.startswith("WG"):
        print("標品　　{}を読み込み中...".format(filename))
        g_names.append(filename.split("_")[0])
        if g_first:
            g_ref = pd.read_csv(os.path.join(ref_dir, filename), header = None, index_col = 0)
            g_ref = g_ref.rename(columns={1:filename.split("_")[0], 0:""})
            g_ref = g_ref.T
            g_first = False
        else:
            other_g = pd.read_csv(os.path.join(ref_dir, filename), header = None, index_col = 0)
            other_g = other_g.rename(columns={1:filename.split("_")[0], 0:""})
            other_g = other_g.T
            g_ref = g_ref.append(other_g)
    elif filename.startswith("WK"):
        print("標品　　{}を読み込み中...".format(filename))
        k_names.append(filename.split("_")[0])
        if k_first:
            k_ref = pd.read_csv(os.path.join(ref_dir, filename), header = None, index_col = 0)
            k_ref = k_ref.rename(columns={1:filename.split("_")[0], 0:""})
            k_ref = k_ref.T
            k_first = False
        else:
            other_k = pd.read_csv(os.path.join(ref_dir, filename), header = None, index_col = 0)
            other_k = other_k.rename(columns={1:filename.split("_")[0], 0:""})
            other_k = other_k.T
            k_ref = k_ref.append(other_k)
    else:
        print("不適切なファイルを検出")
        continue
#TODO:TCCの類似度を格納するCSVファイルを作成する
now = datetime.datetime.now()
title_g = '{0}_similarity_g_{1:%Y%m%d%H}.csv'.format(data_from, now)
title_k = '{0}_similarity_k_{1:%Y%m%d%H}.csv'.format(data_from, now)
csv_file_obj_g = open(os.path.join(sim_dir, title_g), "w", newline = "", encoding = "utf-8")
csv_file_obj_k = open(os.path.join(sim_dir, title_k), "w", newline = "", encoding = "utf-8")
writer_g = csv.writer(csv_file_obj_g)
writer_k = csv.writer(csv_file_obj_k)
header = ["sample", "most similar"]
header_g = header + g_names
header_k = header + k_names
writer_g.writerow(header_g)
writer_k.writerow(header_k)
    
#TODO:ファイルを抜き出してループ
for filename in os.listdir(sample_dir):
    if filename.startswith(("WG", "G")):
        filetype = "gasoline"
    elif filename.startswith(("K", "WK")):
        filetype = "kerosene"
    else:                   #ガソリン灯油に関係ないファイルは飛ばす
        filetype = "other"
        print("不適切なファイルを検出")
        continue
    data = pd.read_csv(os.path.join(sample_dir, filename), header = None, index_col = 0)
    intensity = np.array(data[1])
    intensity = intensity*norm/max(intensity)
    print("サンプル{}を読み込み中...".format(filename))
    filedata =[]
    filedata.append(filename.split("_")[0])

#TODO:標品の数だけループして類似度を計算
    similarity = []
    highest = 0
    most_similar = [""]
    if filetype == "gasoline":
        ref = g_ref
    elif filetype == "kerosene":
        ref = k_ref
    else:
        print("不適切なファイルを検出")
        continue
    for i in ref.T:
        ref_intensity = np.array(ref.loc[i])
        ref_intensity = ref_intensity*norm/max(ref_intensity)
        sim = round(euclid_sim(intensity, ref_intensity),2)
        similarity.append(sim)
        if sim > highest:
            highest = sim
            most_similar[0] = i
    most_similar.extend(similarity)
    filedata.extend(most_similar)
    if filetype == "gasoline":
        writer_g.writerow(filedata)
    elif filetype == "kerosene":
        writer_k.writerow(filedata)

csv_file_obj_g.close()
csv_file_obj_k.close()

"""
Created on Tue Mar 24 16:15:10 2020

@author: Chem3-MT
"""

