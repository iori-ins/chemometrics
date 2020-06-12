# -*- coding: utf-8 -*-
"""
テキスト用の比較画像を作成するプログラム
リストに挙げたファイルを縦に重ねて描画する
"""
import os
os.chdir(os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA"))
import matplotlib.pyplot as plt
import tool

#ディレクトリの指定
fig_dir     = os.path.abspath(r"C:/Users/Chem3-MT/Documents/04.プログラミング/Python/油類鑑定/AIA/fortext/fig")
source_dir  = os.path.abspath(r"C:/Users/Chem3-MT/Documents/04.プログラミング/Python/油類鑑定/AIA/GCMS_csv")

#定数の指定(omajinai) 
k_scope = (2,12)
g_scope = (2,10)
fig_type = ("WG","WK", "GA", "GB", "GC", "KA", "KB", "KC")
type_dict = {"G": "gasoline", "K":"kerosene", "A":" - flooring", "B":" - carpet", "C":" - tatami", "W":""}
weth_dict = {"01":"today", "02":"1 day", "03":"3 days", "04":"1 week", "05":"2 weeks",
             "06":"1 month", "07":"2 months", "08":"3 months", "09":"6 months",
             "0":"neat", "50":"50% weathered", "75":"75% weathered", "90":"90% weathered", "99":"99% weathered"}

#作成する画像に応じた定数・ファイル名
file_list = ()  #描画するファイル名(描画順)
label_list = []    #TICの右肩に入れるサンプル名
scope = (2,12)
title = ""      #保存するファイル名

    
#先にクロマトグラムのサイズだけを決めておく
height = 1.2*len(file_list) 
fig = plt.figure(figsize=(3.6, height))
#下軸ラベルがずれるので、試料数に応じてオフセットを調整
fig.text(0.5, 0.05, "Retention time (min)", ha = "center", transform = fig.transFigure)#0.05
fig.text(0.5, 0.9, title, ha = "center", transform = fig.transFigure)
fig.text(0.07, 0.5, 'Relative intensity', rotation='vertical', va='center', transform = fig.transFigure)
print("描画中......")

#読みだすファイルをループする
fig_num = 1
for csv_file in file_list:
    #ファイルから保持時間と強度を読み取る
    csv_dir = os.path.join(source_dir, csv_file)
    tic_data = tool.get_tic(csv_dir)
    #TODO:RTの読み込みと描画範囲にあたるindexの取り出し
    start_index = 0
    end_index = -1
    for i in range(len(tic_data[0])):
        if scope[0] < tic_data[0][i]:
            start_index = i-1
            break
    for i in range(len(tic_data[0])):
        if scope[1] <= tic_data[0][i]:
            end_index = i
            break
    #描画範囲の最大値を取り出す
    max_intensity = max(tic_data[1][start_index:end_index])
    
    #プロット
    ax = fig.add_subplot(len(file_list), 1, fig_num)
    ax.plot(tic_data[0], tic_data[1], color = "black", linewidth = 0.3)
    ax.set_xlim(scope)
    ax.set_ylim(0, max_intensity*1.1)  
    ax.set_yticks([])
    ax.grid(False)
    ax.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
    #サンプル名を右肩に入れる
    fig.text(0.995, 0.95, label_list[fig_num-1], ha = "right", va = "top", transform=ax.transAxes)
    #最後のプロットの際に
    if fig_num == len(file_list):
        ax.tick_params(labelbottom=True)
    fig_num +=1

#pngとして保存
fig_name = title + r".png"
plt.subplots_adjust(wspace = 0, hspace = 0)
plt.savefig(os.path.join(fig_dir,fig_name), dpi=350, bbox_inches = "tight")
plt.show()
plt.close()

"""
Created on Thu May 28 08:57:07 2020

@author: Chem3-MT
"""

