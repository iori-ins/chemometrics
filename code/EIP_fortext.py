# -*- coding: utf-8 -*-
"""
ファイル1つから指定したEIPを作成する。
テキスト用のデータ出力
"""
import os, sys
os.chdir(os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA"))
import matplotlib.pyplot as plt
import tool

#ディレクトリの指定
fig_dir     = os.path.abspath(r"C:/Users/Chem3-MT/Documents/04.プログラミング/Python/油類鑑定/AIA/fortext/eip")
source_dir  = os.path.abspath(r"C:/Users/Chem3-MT/Documents/04.プログラミング/Python/油類鑑定/AIA/GCMS_csv")
filename = "LPHDPEO4.csv"
csv_dir = os.path.join(source_dir, filename)

if not os.path.exists(csv_dir):
    print("{} は存在ません。ファイル名を確認して下さい".format(filename))
    sys.exit()

#定数の指定
scope = (4,14)
fragment = (0, 57, 71, 55, 69)
#プロットのサイズ
height = 1.2 * (len(fragment)+1)
width = 3.6
 
#TODO:ファイルの読み込み
title = filename.split(".")[0]
print("描画中......{}".format(filename))
tic_data = tool.get_tic(csv_dir)

#TODO:RTの読み込みと描画範囲にあたるindexの取り出し
start_index = 0
end_index = -1
for i in range(len(tic_data[0])):
    if scope[0] < tic_data[0][i]:
        start_index = i-1
        if start_index < 0:
            start_index = 0
        break
for i in range(len(tic_data[0])):
    if scope[1] <= tic_data[0][i]:
        end_index = i
        break
    
#TODO:最大強度のピークを抜き出す    
max_intensity = max(tic_data[1][start_index:end_index])
#TODO:描画設定を定める
fig = plt.figure(figsize=(width, height))
fig.text(0.5, 0.19, "Retention time (min)", ha = "center", transform = fig.transFigure)
fig.text(0.5, 0.89, title, ha = "center", transform = fig.transFigure)
fig.text(0.07, 0.5, 'Intensity', rotation='vertical', va='center', transform = fig.transFigure)
fig_num = 1

#TODO:EIP用の最大強度を取得する
eip_max = 0
for mz in fragment:
    if mz == 0:
        continue
    else:
        data = tool.get_eic(csv_dir, mz)
        temp_max = max(data[1][start_index:end_index])
        if temp_max > eip_max:
            eip_max = temp_max
#TODO:フラグメントイオンをループして描画する        
for mz in fragment:
    if mz ==0:
        data = tool.get_tic(csv_dir)
        s_name = "TICC"
    else:
        data = tool.get_eic(csv_dir, mz)
        s_name = r"m/z=" + str(mz)
        max_intensity =eip_max
    #実際の描画
    ax = fig.add_subplot((len(fragment)+1), 1, fig_num)
    ax.plot(data[0], data[1], color = "black", linewidth = 0.3)
    ax.set_xlim(scope)
    ax.set_ylim(0, max_intensity*1.1)  
    ax.set_yticks([])
    ax.grid(False)
    ax.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
    #サンプル名を右肩に入れる
    fig.text(0.995, 0.95, s_name, ha = "right", va = "top", transform=ax.transAxes)
    #最後のプロットの際に
    if fig_num == len(fragment):
        ax.tick_params(labelbottom=True)
    fig_num +=1

#TODO:出力
fig_name = title + r".png"
plt.subplots_adjust(wspace = 0, hspace = 0)
plt.savefig(os.path.join(fig_dir,fig_name), dpi=350, bbox_inches = "tight")
plt.show()
plt.close()


"""
Created on Thu May 28 15:20:37 2020

@author: Chem3-MT
"""

