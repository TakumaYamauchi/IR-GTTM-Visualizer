"""IR情報量とGTTM情報量を計算するためのメソッドクラス"""

import math
import copy
from IR_GTTM_Analyzer import ir

class CalcEntropy():
    def __init__(self):
        pass

    """pitchとclosure_pitch_keyを入力しシンボル列リストを返す"""
    @staticmethod
    def get_symbol_list(pitch_list, closure):
        ir_plot = ir.IR_converter()
        symbol_list = []
        """3つの音高から音程を計算しシンボル列を判定(クロージャ無視)情報量計算に順序や位置は関係ない"""
        for j in range(len(pitch_list) - 2):
            p1 = pitch_list[j]
            p2 = pitch_list[j + 1]
            p3 = pitch_list[j + 2]

            I1 = (p2 - p1)  # 第1音程
            I2 = (p3 - p2)  # 第2音程
            symbol = ir_plot.IR(I1, I2)  # 音程を入力しシンボルに対応する番号を得る(クロージャ無視)

            if j in closure:
                symbol = 8
            if j+1 in closure:
                symbol = 8
            symbol_list.append(symbol)

        return symbol_list


    """実際にIR情報量として使っている"""
    @staticmethod
    def calc_entropy_IR(symbol_list):#symbol_numが分布
        entropy = 0
        symbol_num_new = [380, 3558, 477, 1093, 139, 106, 176, 1646]
        P_X_sum = sum(symbol_num_new)
        P_X = []
        for i in range(len(symbol_num_new)):
            P_X.append(symbol_num_new[i]/P_X_sum)

        for i in range(len(symbol_list)):
            if symbol_list[i]==8:#もしシンボルが'X'だったならパス
                continue
            entropy += -1 * math.log2(P_X[symbol_list[i]])
        return entropy



    "GTTM情報量として使用 総最大タイムスパンを計算"
    @staticmethod
    def calc_entropy_GTTM(duration, rank, parents):
        #durationで重みづけ
        entropy = [0] * (max(rank)+1)
        #rankが最も高いやつが頂点
        #自分の下位に存在する全ての音のdurationの合計
        maximum_timespan_list = copy.copy(duration)#durationで初期化
        for r in range(max(rank)+1):
            for i in range(len(parents)):
                if rank[i] == r:
                    lower = [d for d, x in enumerate(parents) if x == i]#自分より下位の音indexを加える
                    lower.append(i)#自分を加える
                    #print("下位", lower)
                    #lowerに含まれるindexのdurationをすべて計算
                    maximum_timespan = 0
                    for ts in lower:
                        maximum_timespan += maximum_timespan_list[ts]
                    #print("自分の最大タイムスパン", maximum_timespan)#現状だと、直接の下位しかカウントできていない、下の階層からやっていく必要がある
                    maximum_timespan_list[i] = maximum_timespan
        #print("最大タイムスパンリスト", maximum_timespan_list)

        #簡約情報を利用して、簡約レベルごとの総最大タイムスパンを計算
        total_maximum_timespan = sum(maximum_timespan_list)
        entropy[0] = total_maximum_timespan
        for r in range(max(rank)):
            rank_maximum_timespan = 0
            #rankがrの最大タイムスパンindexを取得
            for i, j in enumerate(rank):
                if j == r:
                    rank_maximum_timespan += maximum_timespan_list[i]#このrankでの最大タイムスパンの合計＝簡約によって失われるもの
            total_maximum_timespan -= rank_maximum_timespan
            entropy[r+1] = total_maximum_timespan

        #print("エントロピー", entropy)
        return entropy



    """出現シンボルを用いてシンボルの分布を求める"""
    @staticmethod
    def calc_symbol_distribution(All_symbol_list):
        symbol_count = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(All_symbol_list)):
            for j in range(len(All_symbol_list[i])):
                symbol_count[All_symbol_list[i][j]] += 1
        symbol_sum = sum(symbol_count)
        p_x = symbol_count  # 各シンボルの生起確率を格納したリスト
        for i in range(len(p_x)):
            p_x[i] = p_x[i] / symbol_sum
        return p_x

