# -*- coding: utf-8 -*-
"""
特定の抽出イオンプロファイルをまとめて同じファイルに吐き出す
検出条件を満たすか判別するためのもの
"""
import os
os.chdir(os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA"))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#TODO:ディレクトリの整備
os.makedirs("EIP", exist_ok = True)
eip_dir = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\EIP")
csv_dir = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\GCMS_csv")

#TODO:抽出するイオンとカットオフラインの設定
target_ion = [0, 57, 83, 91, 105, 119, 117, 131, 142, 156] #0はTIC                                             #トップピークに対する比率
mz_range = 0.3                                             #フラグメントイオンの範囲
lower_limit = 34.0                                         #フラグメントイオンの検出下限
scope = (2, 13)                                            #グラフの描画範囲

#TODO:ファイルを抜き出してループ
for filename in os.listdir(csv_dir):
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
    #すでに画像がある場合はスキップ
    if os.path.exists(os.path.join(eip_dir, filename.split(".")[0])):
        continue
    print("{}を読み込み中...".format(filename))
    data = pd.read_csv(os.path.join(csv_dir, filename), header = 0, index_col = 0)
    
#TODO:RTの読み込みと描画範囲にあたるindexの取り出し
    rt = [float(i) for i in list(data.columns)]
    start_index = 0
    end_index = -1
    for i in range(len(rt)):
        if scope[0] < rt[i]:
            start_index = i-1
            break
    for i in range(len(rt)):
        if scope[1] <= rt[i]:
            end_index = i
            break
    
#TODO:指定されたフラグメントイオンだけループする
    for ion in target_ion:
        if ion == 0:
            intensity = np.array(data.loc["total_intensity"])
            title = r"{} TIC".format(filename.split(".")[0])
            
        else:
            number = (ion - lower_limit)*10 + data.index.get_loc(str(lower_limit))           #locでは1024行目以降が読めない
            intensity = np.array(data.iloc[int(number - mz_range*10) : int(number + mz_range*10)])
            title = r"{} m/z = {}".format(filename.split(".")[0], ion)
            for i in range(1, len(intensity)):
                intensity[0] += intensity[i]
            intensity = intensity[0]
        max_intensity = max(intensity[start_index : end_index])
            
#TODO:EIPの描画
        fig = plt.figure(figsize=(6.4, 3.6))
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(rt, intensity, color = "black", linewidth = 0.3)
        ax.set_title(title)
        ax.set_xlabel(r"Retention time (min)")
        ax.set_ylabel(r"Relative intensity")
        ax.set_xlim(scope)
        ax.set_ylim(0, max_intensity*1.1)
        ax.set_yticklabels([])
        plt.tick_params(left=False)

#TODO:クロマトグラムの保存先の整備
        dir_name = os.path.join(eip_dir, filename.split(".")[0])
        ion_dir = os.path.join(eip_dir, str(str(ion) + "_" + filetype))
        os.makedirs(dir_name, exist_ok = True)
        os.makedirs(ion_dir, exist_ok = True)

#TODO:クロマトグラムの保存
        if ion == 0:
            fig_name = title.split(" ")[0] + "_" + "TIC" + r".png"
        else:
            fig_name = title.split(" ")[0] + "_" + title.split(" ")[1].replace("/", "") + str(ion) + r".png"
        plt.savefig(os.path.join(dir_name,fig_name), dpi=350, bbox_inches = "tight")
        plt.savefig(os.path.join(ion_dir,fig_name), dpi=350, bbox_inches = "tight")
        plt.close()

"""
Created on Mon Mar 23 09:12:36 2020

@author: Chem3-MT
"""

