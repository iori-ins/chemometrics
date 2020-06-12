# -*- coding: utf-8 -*-
"""
CDFファイルをCSVファイルに変換するプログラム
"""
import os
os.chdir(os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA"))
from netCDF4 import Dataset
import numpy as np
import collections
import pandas as pd

#TODO:mass_rangeの入力
mr_min = 34
mr_maz = 300

#TODO:ディレクトリの整備
os.makedirs("GCMS_csv", exist_ok = True)
csv_dir = os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA\GCMS_csv")
cdf_dir = os.path.abspath(r"C:/Users/Chem3-MT/Documents/04.プログラミング/Python/油類鑑定/AIA/GCMS_cdf/kasai")
#cdf_dir = os.path.abspath(r"C:/Users/Chem3-MT/Documents/04.プログラミング/Python/油類鑑定/AIA/GCMS_cdf/reference")

#TODO:CDFファイルを取得してループ
for cdf_file in os.listdir(cdf_dir):
    if not cdf_file.endswith(".CDF"):
        continue
#TODO:すでにCSVファイルが作成されていた場合はスキップ
    csv = r"GCMS_csv/" + cdf_file.split(".")[0] + ".csv"
    csv_exist = os.path.exists(csv)
    if csv_exist:
        continue
    print("{}を処理中......".format(cdf_file))
#TODO:CDFファイルを読み込んで必要な値を抽出
    cdf = r"GCMS_cdf/kasai/" + cdf_file
    rootgrp = Dataset(cdf, "r", format = "NETCDF3_CLASSIC")
    var = rootgrp.variables
    scan_number = [int(i) for i in var["actual_scan_number"]]
    scan_time = [round(float(i)/60,3) for i in var["scan_acquisition_time"]]
    total_intensity = [float(i) for i in var["total_intensity"]]
    scan_index = [int(i) for i in var["scan_index"]]
    point_count = [int(i) for i in var["point_count"]]
    mass_values = [round(float(i),2) for i in var["mass_values"]]
    intensity_values = [float(i) for i in var["intensity_values"]]
    fragment_ion_counter = collections.Counter(mass_values)
    fragment_ions = sorted(fragment_ion_counter)
#TODO:データフレームの作成
    mass_range = [i/10 for i in range(mr_min*10,mr_maz*10 + 1)]
    df0 = pd.DataFrame(np.zeros((len(mass_range),len(scan_time))),
                      columns = scan_time,
                      index = mass_range)
    df = pd.DataFrame(total_intensity, 
                       columns = ["total_intensity"],
                       index = scan_time)
    df = df.T
    df = df.append(df0)
#TODO:フラグメントイオンごとに強度を入力
    for i in scan_number:
        for count in range(point_count[i]):
            if mass_values[scan_index[i] + count] <= mr_maz and mass_values[scan_index[i] + count] >= mr_min:
                df.at[mass_values[scan_index[i] + count], scan_time[i]] = intensity_values[scan_index[i] + count]
            else:
                None
#TODO:CSVファイルとして書き出す
    df.to_csv(csv)

"""
Created on Tue Mar 10 08:08:19 2020

@author: Chem3-MT
"""

