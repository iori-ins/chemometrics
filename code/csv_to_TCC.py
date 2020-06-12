# -*- coding: utf-8 -*-
"""
ターゲット化合物クロマトグラム作成プログラム
GCで取得したクロマトグラムのCSVファイルを"csv_files"に入れる。
ターゲット化合物の保持時間は別ファイルから読み込む
ターゲット化合物の相対ピーク面積比をCSVで出力
関数にしてもいいかもしれない
"""

import os
os.chdir(os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA"))
import csv, tool

#TODO:条件のチェック
tc_ex = True      #ターゲット化合物のみを使う場合はFalse、拡張ならTrue
file_check = False  #分析ファイルの選択 Trueならサンプル、Falseなら標品
blank_sub = True   #ブランク減算の有無。Trueなら減算する

#TODO:使用するファイルのディレクトリの確認
blank_dir       = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\similarity\CSV_file\blank")
tc_dir          = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\similarity\TCC\TC_dict")
tcc_dir         = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\similarity\TCC")
csv_dir         = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\similarity\CSV_file")

#識別子の指定
data_from = ""
output = "TCC"
nametag = "_TCC"

#TODO:ターゲット化合物のみを使う場合はtc_exがFalse、拡張ならTrue
gtc_dir         = os.path.join(tc_dir, "gasoline_TC.csv")
ktc_dir         = os.path.join(tc_dir, "kerosene_TC.csv")
if tc_ex:
    output += "_ex"
    nametag += "_ex"
    gtc_dir     = os.path.join(tc_dir, "gasoline_compounds.csv")
    ktc_dir     = os.path.join(tc_dir, "kerosene_compounds.csv")
     
#TODO:ブランク減算の有無。blank_subがTrueなら減算する
if blank_sub:
    output += "_sub"
    nametag += "_sub"
    
#TODO:分析ファイルの選択 file_checkがTrueならサンプル、Falseなら標品
if file_check:
    data_from = "sample"
    output += "_sample"
else:
    data_from = "refference"
    output += "_refference"

#csvファイルの読み込み元、TCCファイルの出力先を指定    
csv_files = os.path.join(csv_dir, data_from)
output_dir = os.path.join(tcc_dir, output)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)     
     
#TODO:ターゲット化合物と保持時間の辞書を読み込む
gasoline_tc = {}
kerosene_tc = {}
with open(gtc_dir, "r", newline="") as gtc:
    reader = csv.reader(gtc)
    for row in reader:
        gasoline_tc[float(row[0])] = row[1]
        
with open(ktc_dir, "r", newline="") as ktc:
    reader = csv.reader(ktc)
    for row in reader:
        kerosene_tc[float(row[0])] = row[1]

#TODO:読み込んだ辞書から保持時間とターゲット化合物の名前を読み出す
gasoline_rt = sorted(gasoline_tc.keys())
kerosene_rt = sorted(kerosene_tc.keys())
gasoline_tcname = []
for tc_rt in gasoline_rt:
    gasoline_tcname.append(gasoline_tc[tc_rt])
kerosene_tcname = []
for tc_rt in kerosene_rt:
    kerosene_tcname.append(kerosene_tc[tc_rt])

#TODO:csv_file中のファイル数だけループする
for csv_file in os.listdir(csv_files):
    print("{}のTCCを作成中...".format(csv_file))

#TODO:CSVを読み込んでピーク情報を得る
    target_file_dir = os.path.join(csv_files, csv_file)
    if blank_sub:
        peak_info = tool.pick2(target_file_dir, blank_dir)
    else:
        peak_info = tool.pick(target_file_dir)
    start = []
    end = []
    peak_area = []
    for i in peak_info:
        start.append(i[0])
        end.append(i[1])
        peak_area.append(i[2])

#TODO:gasolineとkeroseneのTCのピーク面積を獲得する
    if csv_file.startswith(("G", "WG")):
        target_rt = gasoline_rt
        tc_name = gasoline_tcname
    elif csv_file.startswith(("WK", "K")):
        target_rt = kerosene_rt
        tc_name = kerosene_tcname
    else:
        print("エラー：{}の読み込みに失敗".format(csv_file))
        continue
    tc_peak = []
    for tc_rt in target_rt:
        for rt in start:
            if tc_rt >= rt and tc_rt <= end[start.index(rt)]:
                #print("{}の保持時間は{}～{}でピーク面積は{}".format(gasoline_tc[tc_rt],rt,end[start.index(rt)], peak_area[start.index(rt)]))
                tc_peak.append(peak_area[start.index(rt)])
                break
            elif i == len(start):
                tc_peak.append(0)
            else :
                continue            
    while len(tc_peak) < len(tc_name):
        tc_peak.append(0)

#TODO:ピーク面積の規格化
    tc_stpeak = []
    for peak in tc_peak:
        tc_stpeak.append((100*peak)/sum(tc_peak))

    #TCの名前と規格化したピーク面積のリスト
    tcc_data = list(zip(tc_name,tc_stpeak))

#TODO:ｃｓｖファイルにTCCを出力
    tcc_filename = csv_file.split(".")[0] +nametag + r".csv"
    tcc_file_obj = open(os.path.join(output_dir,tcc_filename), 'w', newline = '')
    tcc_writer =  csv.writer(tcc_file_obj)
    for row in tcc_data:
        tcc_writer.writerow(row)
    tcc_file_obj.close()

"""
Created on Wed Mar 25 16:36:39 2020

@author: Chem3-MT
"""

