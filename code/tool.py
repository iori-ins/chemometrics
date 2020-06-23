# -*- coding: utf-8 -*-
def pick(target_file_dir):
    """"
    読み込むcsvファイルのパスを引数とする
    ピークの開始時間、終了時間、面積、トップピークをlistで返す
    """
    import pandas as pd
    
    target_file= pd.read_csv(target_file_dir, header = 0, index_col = 0)
    rt = [float(i) for i in list(target_file.columns)]
    cur = [float(i)for i in list(target_file.loc["total_intensity"])]
    #currentの差を利用.curを一つ左にずらしたもの
    cur2 = cur[1::] + [0,]     
    dif = []
    for p in range(len(cur)):
        dif.append(cur2[p]-cur[p])
    #ピークの数え上げ
    peak_number = 0     #ピークの数
    start = [rt[0],]    #ピークの開始時刻のリスト
    end = []            #ピークの終了時刻のリスト
    area = 0            #ピークの面積
    peak_area = []      #ピーク面積のリスト
    top_peak = []       #ピークの最高点のrt
    
    #ピークの判別は傾きがマイナスからプラスに転じたかで判定
    for p in range(0,len(dif)):
        if p == 0:
            area += cur[p]
            if dif[p] <= 0:
                top_peak.append(rt[p])
        elif dif[p] <= 0:
            area += cur[p]
            if dif[p-1] > 0:
                top_peak.append(rt[p])
        else:
            if dif[p-1] <= 0:
                area += cur[p]
                peak_number += 1
                end.append(rt[p])
                start.append(rt[p])
                peak_area.append(area)
                area =0
            else:
                area += cur[p]
    peak =list(zip(start,end,peak_area,top_peak))
    return peak

def pick2(target_file_dir, blank_dir):
    """"
    読み込むcsvファイルとブランクのデイレクトリのパスを引数とする
    ピークの開始時間、終了時間、面積、トップピークをlistで返す
    """
    import pandas as pd
    import os
    
    #targe_fileの読み込み
    target_file= pd.read_csv(target_file_dir, header = 0, index_col = 0)   
    rt = [float(i) for i in list(target_file.columns)]
    cur = [float(i)for i in list(target_file.loc["total_intensity"])]
    #blank_dirにあるブランクを全て読み込んで足し合わせる
    is_first = True
    for blank in os.listdir(blank_dir):
        blank_file = pd.read_csv(os.path.join(blank_dir,blank), header = 0, index_col = 0)
        if is_first:
            cur_blank = [float(i)for i in list(blank_file.loc["total_intensity"])]
            is_first = False
        else:
            cur_blank2 = [float(i)for i in list(blank_file.loc["total_intensity"])]
            cur_blank = [i + j for (i,j) in zip (cur_blank, cur_blank2)]
    for i in range(len(cur_blank)):
        cur_blank[i] = round(cur_blank[i]/len(os.listdir(blank_dir)),0)
    #減算を行う
    cur_sub = [(c - b) for (c,b) in zip(cur, cur_blank)]
    for i in cur_sub:
        if i < 0:
            cur_sub[cur_sub.index(i)] = 0
    #currentの差を利用.curを一つ左にずらしたもの
    cur2 = cur_sub[1::] + [0,]     
    dif = []
    for p in range(len(cur_sub)):
        dif.append(cur2[p]-cur_sub[p])
    #ピークの数え上げ
    peak_number = 0     #ピークの数
    start = [rt[0],]    #ピークの開始時刻のリスト
    end = []            #ピークの終了時刻のリスト
    area = 0            #ピークの面積
    peak_area = []      #ピーク面積のリスト
    top_peak = []       #ピークの最高点のrt
    
    #ピークの判別は傾きがマイナスからプラスに転じたかで判定
    for p in range(0,len(dif)):
        if p == 0:
            area += cur_sub[p]
            if dif[p] <= 0:
                top_peak.append(rt[p])
        elif dif[p] <= 0:
            area += cur_sub[p]
            if dif[p-1] > 0:
                top_peak.append(rt[p])
        else:
            if dif[p-1] <= 0:
                area += cur_sub[p]
                peak_number += 1
                end.append(rt[p])
                start.append(rt[p])
                peak_area.append(area)
                area =0
            else:
                area += cur_sub[p]
    peak =list(zip(start,end,peak_area,top_peak))
    return peak

def blank_sub (target_file_dir, blank_dir):
    """"
    読み込むcsvファイルとブランクのデイレクトリのパスを引数とする
    rtと強度をlistで返す
    """
    import pandas as pd
    import os
    
    #targe_fileの読み込み
    target_file= pd.read_csv(target_file_dir, header = 0, index_col = 0, low_memory=False)   
    rt = [float(i) for i in list(target_file.columns)]
    cur = [float(i)for i in list(target_file.loc["total_intensity"])]
    #blank_dirにあるブランクを全て読み込んで足し合わせる
    is_first = True
    for blank in os.listdir(blank_dir):
        blank_file = pd.read_csv(os.path.join(blank_dir,blank), header = 0, index_col = 0)
        if is_first:
            cur_blank = [float(i)for i in list(blank_file.loc["total_intensity"])]
            is_first = False
        else:
            cur_blank2 = [float(i)for i in list(blank_file.loc["total_intensity"])]
            cur_blank = [i + j for (i,j) in zip (cur_blank, cur_blank2)]
    for i in range(len(cur_blank)):
        cur_blank[i] = round(cur_blank[i]/len(os.listdir(blank_dir)),0)
    #減算を行う
    cur_sub = [(c - b) for (c,b) in zip(cur, cur_blank)]
    for i in cur_sub:
        if i < 0:
            cur_sub[cur_sub.index(i)] = 0
    
    return [rt, cur_sub]

def get_tic (target_file_dir):
    """"
    読み込むcsvファイルのパスを引数とする
    保持時間と強度をlistで返す
    """
    import pandas as pd

    #targe_fileの読み込み
    target_file= pd.read_csv(target_file_dir, header = 0, index_col = 0, low_memory=False)   
    rt = [float(i) for i in list(target_file.columns)]
    cur = [float(i)for i in list(target_file.loc["total_intensity"])]
    return [rt, cur]

def get_eic (target_file_dir, mz):
    """"
    読み込むcsvファイルのパスとフラグメントイオンを引数とする
    保持時間と強度をlistで返す
    mzの範囲は0.3
    """
    import pandas as pd
    import numpy as np
    
    #初期値の設定
    mz_range = 0.3

    #targe_fileの読み込み
    target_file= pd.read_csv(target_file_dir, header = 0, index_col = 0, low_memory=False)   
    rt = [float(i) for i in list(target_file.columns)]
    number = (mz - 34.0)*10 + target_file.index.get_loc("34.0")
    total = np.array(target_file.iloc[int(number - mz_range*10) : int(number + mz_range*10)])
    for i in range(1, len(total)):
        total[0] += total[i]
    return [rt, total[0]]

def pick3(target_file_dir):
    """"
    読み込むcsvファイルのパスを引数とする
    ピークの開始時間、終了時間、面積、トップピーク、トップピークの高さをlistで返す
    """
    import pandas as pd
    
    target_file= pd.read_csv(target_file_dir, header = 0, index_col = 0)
    rt = [float(i) for i in list(target_file.columns)]
    cur = [float(i)for i in list(target_file.loc["total_intensity"])]
    #currentの差を利用.curを一つ左にずらしたもの
    cur2 = cur[1::] + [0,]     
    dif = []
    for p in range(len(cur)):
        dif.append(cur2[p]-cur[p])
    #ピークの数え上げ
    peak_number = 0     #ピークの数
    start = [rt[0],]    #ピークの開始時刻のリスト
    end = []            #ピークの終了時刻のリスト
    area = 0            #ピークの面積
    peak_area = []      #ピーク面積のリスト
    top_peak = []       #ピークの最高点のrt
    peak_height = []
    #ピークの判別は傾きがマイナスからプラスに転じたかで判定
    for p in range(0,len(dif)):
        if p == 0:
            area += cur[p]
            if dif[p] <= 0:
                top_peak.append(rt[p])
                peak_height.append(cur[p])
        elif dif[p] <= 0:
            area += cur[p]
            if dif[p-1] > 0:
                top_peak.append(rt[p])
                peak_height.append(cur[p])
        else:
            if dif[p-1] <= 0:
                area += cur[p]
                peak_number += 1
                end.append(rt[p])
                start.append(rt[p])
                peak_area.append(area)
                area =0
            else:
                area += cur[p]
    peak =list(zip(start,end,peak_area,top_peak,peak_height))
    return peak

def euclid_sim(v1, v2):
    import numpy as np
    e_distance = np.linalg.norm(v1-v2)
    return (1 - e_distance)

def pearson_sim(v1, v2):
    import numpy as np
    cov = np.cov(v1,v2)[0][1]
    std_v1 = np.std(v1)
    std_v2 = np.std(v2)
    pearson = cov/(std_v1*std_v2)
    return pearson

def pick4(target_file_dir):
    """"
    読み込むcsvファイルのパスを引数とする
    ピークの開始時間、終了時間、面積、トップピーク、トップピークの高さをlistで返す
    強度が最大ピークの100分の一以下のピークを除去する
    """
    import pandas as pd
    
    target_file= pd.read_csv(target_file_dir, header = 0, index_col = 0)
    rt = [float(i) for i in list(target_file.columns)]
    cur = [float(i)for i in list(target_file.loc["total_intensity"])]
    #最大強度の100分の1以下のピークを排除
    rejection = max(cur)/100
    temp = []
    for i in cur:
        if i >= rejection:
            temp.append(i)
        else:
            temp.append(0)
    cur = temp
    #currentの差を利用.curを一つ左にずらしたもの
    cur2 = cur[1::] + [0,]     
    dif = []
    for p in range(len(cur)):
        dif.append(cur2[p]-cur[p])
    #ピークの数え上げ
    peak_number = 0     #ピークの数
    start = [rt[0],]    #ピークの開始時刻のリスト
    end = []            #ピークの終了時刻のリスト
    area = 0            #ピークの面積
    peak_area = []      #ピーク面積のリスト
    top_peak = []       #ピークの最高点のrt
    peak_height = []
    #ピークの判別は傾きがマイナスからプラスに転じたかで判定
    for p in range(0,len(dif)):
        if p == 0:
            area += cur[p]
            if dif[p] <= 0:
                top_peak.append(rt[p])
                peak_height.append(cur[p])
        elif dif[p] <= 0:
            area += cur[p]
            if dif[p-1] > 0:
                top_peak.append(rt[p])
                peak_height.append(cur[p])
        else:
            if dif[p-1] <= 0:
                area += cur[p]
                peak_number += 1
                end.append(rt[p])
                start.append(rt[p])
                peak_area.append(area)
                area =0
            else:
                area += cur[p]
    peak =list(zip(start,end,peak_area,top_peak,peak_height))
    return peak

def get_tic_cutoff (target_file_dir):
    """"
    読み込むcsvファイルのパスを引数とする
    保持時間と強度をlistで返す
    """
    import pandas as pd

    #targe_fileの読み込み
    target_file= pd.read_csv(target_file_dir, header = 0, index_col = 0, low_memory=False)   
    rt = [float(i) for i in list(target_file.columns)]
    cur = [float(i)for i in list(target_file.loc["total_intensity"])]
    rejection = max(cur)/100
    temp = []
    for i in cur:
        if i >= rejection:
            temp.append(i)
        else:
            temp.append(0)
    cur = temp
    return [rt, cur]

"""
Created on Wed Mar 25 16:33:29 2020

@author: Chem3-MT
"""

