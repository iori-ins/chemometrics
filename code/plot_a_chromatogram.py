# -*- coding: utf-8 -*-
"""
指定したディレクトリ中の全てのcsvのTICを描画する
"""

import os
os.chdir(os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA"))
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
#from matplotlib.ticker import AutoLocator
import tool

#ディレクトリの指定
source_dir  = os.path.abspath(r"C:/Users/Chem3-MT/Documents/04.プログラミング/Python/油類鑑定/AIA/GCMS_csv")
tic_dir     = os.path.abspath(r"C:/Users/Chem3-MT/Documents/04.プログラミング/Python/油類鑑定/AIA/fortext/tic")

#描画範囲指定
scope = (2.1,18)

#file_listで読み込むファイルを指定する(任意)
file_list = os.listdir(source_dir)
file_list = [i for i in os.listdir(source_dir) if i.startswith("R")]

#CSVのあるディレクトリを指定してループ
for csv_file in file_list:
    print("描画中......{}".format(csv_file))
    csv_dir = os.path.join(source_dir, csv_file)
    tic_data = tool.get_tic(csv_dir)
    
    #TODO:RTの読み込みと描画範囲にあたるindexの取り出し
    start_index = 0
    end_index = -1
    for i in range(len(tic_data[0])):
        if scope[0] < tic_data[0][i]:
            start_index = i-1
            if start_index <0:
                start_index =0
            break
    for i in range(len(tic_data[0])):
        if scope[1] <= tic_data[0][i]:
            end_index = i
            break
    #描画に必要な値の計算
    title = csv_file.split(".")[0] + "_TIC"
    max_intensity = max(tic_data[1][start_index:end_index])
    
    #プロット
    fig = plt.figure(figsize=(6.4, 3.6))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(tic_data[0], tic_data[1], color = "black", linewidth = 0.3)
    ax.set_title(title)
    ax.set_xlabel(r"Retention time (min)")
    ax.set_ylabel(r"Relative intensity")
    ax.set_xlim(scope)
    ax.set_ylim(0, max_intensity*1.1)        
    ax.grid(False)
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
    #ax.yaxis.set_major_locator(AutoLocator)

    #pngとして保存
    fig_name = title + r".png"
    plt.savefig(os.path.join(tic_dir,fig_name), dpi=350, bbox_inches = "tight")
    plt.close()

"""
Created on Mon Mar 30 11:51:49 2020

@author: Chem3-MT
"""

