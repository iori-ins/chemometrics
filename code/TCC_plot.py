# -*- coding: utf-8 -*-
"""
TCCのCSVファイルからTCCをプロットしてpngファイルに保存する
"""
import matplotlib.pyplot as plt
import csv, os
import numpy as np
import seaborn as sns
os.chdir(os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA"))

#TODO:条件のチェック
tc_ex = True       #拡張ターゲット化合物はが使用されているか。拡張ならTrue
blank_sub = True   #TCCファイルが減算されているか。減算されているならTrue

#TODO:ディレクトリの整備
tcc_dir     = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\similarity\TCC")
plot_dir    = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\similarity\TCC_plot")

#読み込むファイルの指定
output = "TCC"
if tc_ex:
    output += "_ex"
if blank_sub:
    output += "_sub"
ref = output + "_refference"
sample = output + "_sample"
output += "_plot"
output_dir = os.path.join(plot_dir, output)
ref_dir = os.path.join(tcc_dir, ref)
sample_dir = os.path.join(tcc_dir,sample)
dir_list = [ref_dir, sample_dir]

#TODO:プロットするTCCのCSVファイルの数だけループ
for tcc_dir in dir_list:
    for tcc_file in os.listdir(tcc_dir):
        print("{}のTCCを出力中......".format(tcc_file))
        file_obj = open(os.path.join(tcc_dir, tcc_file), "r", encoding = "utf-8")
        reader = csv.reader(file_obj)
        
#TODO:ファイルからTCとピーク面積を抜き出す    
        stpeaks = []
        tc = []
        for row in reader:
            stpeaks.append(float(row[1]))
            tc.append(row[0])
        file_obj.close()

#TODO:使用するTCのタイプ
        if tcc_file.startswith(("WG", "G")):
            tc_type = "gasoline"
        elif tcc_file.startswith(("WK", "K")):
            tc_type = "kerosene"
        else:
            print("error")

#TODO:棒グラフの描画設定        
        sns.set()
        sns.set_style("whitegrid")
        sns.set_palette("gray")
        x_position = np.arange(len(tc))
        titles = tcc_file.split("_")[0]
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1, title = titles)
        ax.barh(x_position, stpeaks, tick_label = tc)
        ax.set_ylabel("Target Compounds for {}".format(tc_type))
        plot_png = tcc_file.split(".")[0] + r".png"
        plt.savefig(os.path.join(output_dir,plot_png), dpi = 400, bbox_inches = "tight")
        plt.close()

"""
Created on Fri Mar 27 10:23:20 2020

@author: Chem3-MT
"""

