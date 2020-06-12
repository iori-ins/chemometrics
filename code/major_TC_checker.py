# -*- coding: utf-8 -*-
"""
TCCで存在比が１０%以上の化合物を出力する。
一応上から５つまでリストアップ
"""
import csv, os
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
output_dir = os.path.join(plot_dir, output)
ref_dir = os.path.join(tcc_dir, ref)
sample_dir = os.path.join(tcc_dir,sample)
dir_list = [ref_dir, sample_dir]

#TODO:保存するCSVファイルを開いておく
filename = "major_" + output + ".csv"
csv_obj = open(os.path.join(plot_dir, filename), "w", newline = "", encoding = "utf-8")
writer = csv.writer(csv_obj)

for tcc in dir_list:
    for tcc_file in os.listdir(tcc):
        file_obj = open(os.path.join(tcc, tcc_file), "r", encoding = "utf-8")
        reader = csv.reader(file_obj)
        major = [row[0] for row in reader if float(row[1])>=10]
        name = [tcc_file.split("_")[0]]
        name.extend(major)
        writer.writerow(name)
        file_obj.close()
csv_obj.close()

"""
Created on Thu Apr  2 16:17:13 2020

@author: Chem3-MT
"""

