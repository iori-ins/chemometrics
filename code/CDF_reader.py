# -*- coding: utf-8 -*-

import os
os.chdir(os.path.abspath(r"C:\Users\Chem3-MT\Documents\04.プログラミング\Python\油類鑑定\AIA"))
from netCDF4 import Dataset
import numpy as np
import collections
import pandas as pd

#TODO:mass_rangeの入力
mr_min = 34
mr_maz = 300
cdf_dir = r"GCMS_cdf/WG0-N1.CDF"
#TODO:
rootgrp = Dataset(cdf_dir, "r", format = "NETCDF3_CLASSIC")
dim = rootgrp.dimensions
var = rootgrp.variables
keys = var.keys()
#TODO:値の抽出
scan_number = [int(i) for i in var["actual_scan_number"]]
scan_time = [round(float(i)/60,3) for i in var["scan_acquisition_time"]]
total_intensity = [float(i) for i in var["total_intensity"]]
scan_index = [int(i) for i in var["scan_index"]]
point_count = [int(i) for i in var["point_count"]]
mass_values = [round(float(i),2) for i in var["mass_values"]]
intensity_values = [float(i) for i in var["intensity_values"]]
fragment_ion_counter = collections.Counter(mass_values)
fragment_ions = sorted(fragment_ion_counter)
mass_range_max = [round(float(i),2) for i in var["mass_range_max"]]

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
"""
Created on Fri Mar  6 09:00:04 2020

@author: Chem3-MT
"""

