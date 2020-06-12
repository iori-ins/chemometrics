# -*- coding: utf-8 -*-
"""
TICと抽出イオンプロファイルを縦長に描写する
萩原さんの論文用
"""
import os, re
os.chdir(os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA"))
import matplotlib.pyplot as plt
import tool

#ディレクトリの指定
fig_dir     = os.path.abspath(r"C:/Users/Chem3-MT/Documents/04.プログラミング/Python/油類鑑定/AIA/article_fig/hagiwara3")
source_dir  = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\article_fig\plot_source")

#定数の指定
k_scope = (2,12)
g_scope = (2,10)
fig_type = ("WG","WK", "GA", "GB", "GC", "KA", "KB", "KC")
type_dict = {"G": "gasoline", "K":"kerosene", "A":"-flooring", "B":"-carpet", "C":"-tatami", "W":""}
weth_dict = {"01":"today", "02":"1 day", "03":"3 days", "04":"1 week", "05":"2 weeks",
             "06":"1 month", "07":"2 months", "08":"3 months", "09":"6 months",
             "0":"neat", "50":"50% weathered", "75":"75% weathered", "90":"90% weathered", "99":"99% weathered"}
g_fragment = (0, 57, 83, 91, 105 ,119, 117, 131, 142)
k_fragment = (0, 57, 71 ,85, 99, 83, 91, 105, 119)
#プロットのサイズ
g_height = 1.2 * (len(g_fragment)+1)
k_height = 1.2 * (len(k_fragment)+1)
width = 3.6

#TODO:source_dirにあるファイルをループ。1つごとに１枚画像を描画する
for csv_file in os.listdir(source_dir):
    
    #液体の種類に応じて描画範囲を決定する.名前も決定する
    if csv_file.startswith(("WG","G")):
        scope = g_scope
        height = g_height
        fragment = g_fragment
    else:
        scope = k_scope
        height = k_height
        fragment = k_fragment
    l_type = re.search(r"[K,G]", csv_file)
    f_type = re.search(r"[A,B,C,W]", csv_file)
    weth = re.search(r"\d+", csv_file)
    title = type_dict[l_type.group()] + type_dict[f_type.group()] + r"-" + weth_dict[weth.group()]
    #TODO:ファイルの読み込み
    print("描画中......{}".format(csv_file))
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
    #TODO:最大強度のピークを抜き出す    
    max_intensity = max(tic_data[1][start_index:end_index])
    #TODO:描画設定を定める
    fig = plt.figure(figsize=(width, height))
    fig.text(0.5, 0.168, "Retention time (min)", ha = "center", transform = fig.transFigure)
    fig.text(0.5, 0.89, title, ha = "center", transform = fig.transFigure)
    fig.text(0.07, 0.5, 'Relative intensity', rotation='vertical', va='center', transform = fig.transFigure)
    fig_num = 1
    
    #TODO:フラグメントイオンをループして描画する
    for mz in fragment:
        if mz ==0:
            data = tool.get_tic(csv_dir)
            s_name = "TICC"
        else:
            data = tool.get_eic(csv_dir, mz)
            s_name = r"m/z=" + str(mz)
        max_intensity = max(data[1][start_index:end_index])
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
Created on Thu Apr 30 09:05:04 2020

@author: Chem3-MT
"""

