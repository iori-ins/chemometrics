# -*- coding: utf-8 -*-
"""
Target compoundsを自動検出して
クロマトグラム上の当該ピークに化合物名のラベルを張り付ける
"""

import matplotlib.pyplot as plt
import csv, os, re
os.chdir(os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA"))
import tool

#TODO:ディレクトリの整備
source_dir  = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\article_fig\plot_source")
fig_dir     = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\article_fig\TIC_with_label")
tc_dir      = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\similarity\TCC\TC_dict")
gtc_dir     = os.path.join(tc_dir, "gasoline_compounds_article.csv")
ktc_dir     = os.path.join(tc_dir, "kerosene_compounds.csv")

#描画範囲、試料のタイプの入力
k_scope = (2,12)
g_scope = (3.5,8.5)
fig_type = ("WG","WK", "GA", "GB", "GC", "KA", "KB", "KC")
type_dict = {"G": "gasoline", "K":"kerosene", "A":" - flooring", "B":" - carpet", "C":" - tatami", "W":""}
weth_dict = {"01":"today", "02":"1 day", "03":"3 days", "04":"1 week", "05":"2 weeks",
             "06":"1 month", "07":"2 months", "08":"3 months", "09":"6 months",
             "0":"neat", "50":"50% weathered", "75":"75% weathered", "90":"90% weathered", "99":"99% weathered"}

#TODO:ターゲット化合物と保持時間の辞書を読み込んで名前を抜き出す
gasoline_tc = {}
with open(gtc_dir, "r", newline="") as gtc:
    reader = csv.reader(gtc)
    for row in reader:
        gasoline_tc[float(row[0])] = row[1]
gasoline_rt = sorted(gasoline_tc.keys())
gasoline_tcname = []
for tc_rt in gasoline_rt:
    gasoline_tcname.append(gasoline_tc[tc_rt])
kerosene_tc = {}
with open(ktc_dir, "r", newline="") as ktc:
    reader = csv.reader(ktc)
    for row in reader:
        kerosene_tc[float(row[0])] = row[1]
kerosene_rt = sorted(kerosene_tc.keys())
kerosene_tcname = []
for tc_rt in kerosene_rt:
    kerosene_tcname.append(kerosene_tc[tc_rt])


#source_dirにあるcsv_fileをループで回す
for csv_file in os.listdir(source_dir):
    print("{}のクロマトグラムを作成中...".format(csv_file))
    l_type = re.search(r"[K,G]", csv_file)
    f_type = re.search(r"[A,B,C,W]", csv_file)
    title = type_dict[l_type.group()] + type_dict[f_type.group()]
    weth = re.search(r"\d+", csv_file)
    title += " " + weth_dict[weth.group()]
    #ファイルの種類に応じて参照するターゲット化合物辞書を選ぶ
    if csv_file.startswith(("WG", "G")):
        tc_rt = gasoline_rt
        tc_name = gasoline_tcname
        scope = g_scope
    elif csv_file.startswith(("WK", "K")):
        tc_rt = kerosene_rt
        tc_name = kerosene_tcname
        scope = k_scope
    #ファイルlからピーク情報を読み込んでlistにする
    peak_info = tool.pick3(os.path.join(source_dir, csv_file))
    peak_start = [i[0] for i in peak_info]
    peak_end = [i[1] for i in peak_info]
    peak_area = [i[2] for i in peak_info]
    peak_top = [i[3] for i in peak_info]
    peak_top_height = [i[4] for i in peak_info]
    #ファイルからTICを読み込む
    tic_data = tool.get_tic(os.path.join(source_dir, csv_file))
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
    
    #target compoundだけ回して該当するピークと抜き出す
    compound_rt = []
    compound_top_height = []
    for tc in tc_rt:
        for rt in peak_start:
            if tc >= rt and tc <= peak_end[peak_start.index(rt)]:
                compound_rt.append(peak_top[peak_start.index(rt)])
                compound_top_height.append(peak_top_height[peak_start.index(rt)])
                break
            elif rt == peak_start[-1]:
                compound_rt.append(peak_top[peak_start.index(rt)])
                compound_top_height.append(peak_top_height[peak_start.index(rt)])
                break
            else:
                continue
    compound_data = list(zip(range(1,len(tc_name)+1), tc_name, compound_rt,compound_top_height))
         
    #TODO:scopeに合うようにラベルを作成する        
    limited_data =  []
    label = [""]
    for compound in compound_data:
        if compound[2] > scope[1]:
            break
        limited_data.append(compound)
        label[0] += "{} : {}\n".format(compound[0], compound[1])
#TODO:クロマトグラムの描写
    fig = plt.figure(figsize=(6.4, 3.6))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(tic_data[0], tic_data[1], color = "black", linewidth = 0.3)
    ax.set_title(title)
    ax.set_xlabel(r"Retention time (min)")
    ax.set_ylabel(r"Rerative intensity")
    ax.set_xlim(scope)
    ax.set_ylim([0, max_intensity*1.3])
    ax.set_yticks([])
    ax.tick_params(labelbottom=True, labelleft=False, labelright=False, labeltop=False)
    ax.legend(loc = "upper left", bbox_to_anchor = (1.05, 1),
              labels = label, handlelength = 0)

#TODO:ラベルの付与
    pre_rt = 0
    pre_height = 0
    default = max_intensity*0.20
    #short = max_intensity*0.15
    for number, name, acrt, height in limited_data:
        arrowlen = default
        shift = 0
        if (acrt - pre_rt) <= 0.11 and abs(height - pre_height) < arrowlen/2:
            shift = 0.1
        if number == 12 or number == 20:
            shift = -0.1
        elif number == 13:
            shift = 0
            arrowlen = max_intensity*0.30
        elif number == 21:
            shift = 0
            arrowlen = max_intensity*0.20
        ax.annotate(number, xy = (float(acrt), height + max_intensity*0.005),
                    xytext = (acrt + shift, height + arrowlen),
                    arrowprops = dict(arrowstyle = "->", facecolor = "black"),
                    horizontalalignment = "center", verticalalignment = "top",
                    fontsize = 8)
        pre_rt = acrt
        pre_height = height

#TODO:画像をpng出力して保存する
    filename = csv_file.split(".")[0] + r".png"
    #plt.show()
    plt.savefig(os.path.join(fig_dir, filename), dpi=400, bbox_inches = "tight")
    plt.close()

"""
Created on Fri Apr  3 09:08:11 2020

@author: Chem3-MT
"""

