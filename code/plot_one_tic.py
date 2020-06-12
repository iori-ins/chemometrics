# -*- coding: utf-8 -*-

import os
os.chdir(os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA"))
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
#from matplotlib.ticker import AutoLocator
import tool

source_dir  = os.path.abspath(r"C:/Users/Chem3-MT/Documents/04.プログラミング/Python/油類鑑定/AIA/GCMS_csv")
fig_dir     = os.path.abspath(r"C:/Users/Chem3-MT/Documents/04.プログラミング/Python/油類鑑定/AIA/fortext/tic")
filename    = "LCLP-1.csv"

#描画範囲指定
scope = (2,14)
#mzの指定。0はTIC
mz = 0

#CSVのあるディレクトリを指定してループ
print("描画中......{}".format(filename))
csv_dir = os.path.join(source_dir, filename)
if mz == 0:
    data = tool.get_tic(csv_dir)
    title = filename.split(".")[0] + "_TIC_" + str(scope[0]) + "-" + str(scope[1]) 
else:
    data = tool.get_eic(csv_dir, mz)
    title = filename.split(".")[0] + "_mz{}_".format(mz) + str(scope[0]) + "-" + str(scope[1]) 

#TODO:RTの読み込みと描画範囲にあたるindexの取り出し
start_index = 0
end_index = -1
for i in range(len(data[0])):
    if scope[0] < data[0][i]:
        start_index = i-1
        if start_index < 0:
            start_index = 0
        break
for i in range(len(data[0])):
    if scope[1] <= data[0][i]:
        end_index = i
        break
#描画に必要な値の計算
max_intensity = max(data[1][start_index:end_index])

#プロット
fig = plt.figure(figsize=(6.4, 3.6))
ax = fig.add_subplot(1, 1, 1)
ax.plot(data[0], data[1], color = "black", linewidth = 0.3)
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
plt.savefig(os.path.join(fig_dir,fig_name), dpi=350, bbox_inches = "tight")
plt.show()
plt.close()
"""
Created on Mon May 11 13:22:00 2020

@author: Chem3-MT
"""

