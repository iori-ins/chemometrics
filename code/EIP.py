# -*- coding: utf-8 -*-
import os
os.chdir(os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA"))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#TODO:ディレクトリの整備
os.makedirs("EIP", exist_ok = True)
eip_dir = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\EIP")
target_file =  "G200212.csv"
csv_dir = r"GCMS_csv/" + target_file
data = pd.read_csv(csv_dir, header = 0, index_col = 0)
#TODO:抽出するイオン、描画範囲の指定
mz = 117
mz_range = 0.3
draw_range = (4.8, 10.2)
#TODO:RTの調整
rt = [float(i) for i in list(data.columns)]
start_index = 0
end_index = -1
for i in range(len(rt)):
    if draw_range[0] < rt[i]:
        start_index = i-1
        break
for i in range(len(rt)):
    if draw_range[1] <= rt[i]:
        end_index = i
        break
#TODO:指定されたフラグメントイオンを抜き出す
number = (mz - 34.0)*10 + data.index.get_loc("34.0")
total = np.array(data.iloc[int(number - mz_range*10) : int(number + mz_range*10)])
for i in range(1, len(total)):
    total[0] += total[i]

#TODO:描画
max_intensity = max(total[0][start_index : end_index])
order = len(str(int(max_intensity)))-1
y_max = round(((max_intensity*1.1))/(10**order),1)
y_tick = [0]
dif = round(y_max/7, 1)
for i in range(7):
    y_tick.append(round(y_max-dif*i, 1))
y_tick.sort()
fig = plt.figure(figsize=(6.4, 3.6))
ax = fig.add_subplot(1, 1, 1)
ax.plot(rt[start_index : end_index], total[0][start_index : end_index], color = "black", linewidth = 0.3)
ax.set_title(r"{} m/z = {}".format(target_file.split(".")[0], mz))
ax.set_xlabel(r"Retention time (min)")
ax.set_ylabel(r"Relative intensity")
ax.set_xlim([rt[start_index], rt[end_index]])
ax.set_ylim(0, max_intensity*1.1)
ax.set_yticklabels([])
plt.tick_params(left=False)
#ax.set_yticklabels(y_tick)
#plt.locator_params(axis='y',nbins=6)
#ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
#plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
#ax.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))


#TODO:ディレクトリの作成
dir_name = os.path.join(eip_dir, target_file.split(".")[0])
os.makedirs(dir_name, exist_ok = True)

#TODO:画像をpng出力して保存する
filename = target_file.split(".")[0] +"(mz{},".format(mz) + "{}-{})".format(draw_range[0], draw_range[1]) +r".png"
plt.savefig(os.path.join(dir_name,filename), dpi=350, bbox_inches = "tight")
plt.show()
plt.close()

"""
Created on Tue Mar 10 13:22:21 2020

@author: Chem3-MT
"""

