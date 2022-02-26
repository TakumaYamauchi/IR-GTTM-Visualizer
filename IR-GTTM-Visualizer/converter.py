"""各種変換メソッドを格納したクラス"""
import csv
import copy

class Converter():
    PITCH_CLASS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    CLASS_NUMBER = ["-1", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]

    def __init__(self):
        pass

    """csvを読み込みリストを返す(int型)"""
    @staticmethod
    def load_csv_i(path):
        csv_file = open(path, 'r', encoding="shift_jis")
        reader = csv.reader(csv_file, lineterminator='\n')
        load_list_s = [row for row in reader]
        load_list = []
        for i in load_list_s:
            load_list.append([int(s) for s in i])  # durationとsongTitleには使えない
        csv_file.close()
        return load_list

    """csvを読み込みリストを返す(float型)"""
    @staticmethod
    def load_csv_f(path):
        csv_file = open(path, 'r', encoding="shift_jis")
        reader = csv.reader(csv_file, lineterminator='\n')
        load_list_s = [row for row in reader]
        load_list = []
        for i in load_list_s:
            load_list.append([float(s) for s in i])  # durationとsongTitleには使えない
        csv_file.close()
        return load_list

    """csvを読み込みリストを返す(str型)"""
    @staticmethod
    def load_csv_s(path):
        csv_file = open(path, 'r', encoding="utf-8")  # cp932 shift_jis
        reader = csv.reader(csv_file, lineterminator='\n')
        load_list_s = [row for row in reader]
        csv_file.close()
        return load_list_s

    """音高列を音名列に変化させる"""
    @staticmethod
    def No2pitch_list(pitch_list):
        pitch_name_list = []
        PITCH_CLASS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        CLASS_NUMBER = ["-1", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
        for pitch in pitch_list:
            r = pitch % 12
            q = pitch // 12
            name = PITCH_CLASS[r]
            name += CLASS_NUMBER[q]
            pitch_name_list.append(name)
        return pitch_name_list

    # シンボルリストを数字リストからから音程の上下を考慮しないシンボル名のリストに変換する
    @staticmethod
    def get_symbolname_list(symbol_list):  # P_Xは(14,15,1,0,0,3)
        symbol_name_list = []
        SYMBOL_LABEL = ["D", "P", "R", "IP", "VP", "IR", "VR", "ID", "X", "-"]
        for symbol in symbol_list:
            symbol_name_list.append(SYMBOL_LABEL[symbol])
        return symbol_name_list

    """各シンボル数の遷移を記録"""
    @staticmethod
    def get_symbol_transition(symbol_list):
        symbol_change = []  # 音程上下考慮なし #symbol_change[0][0]は簡約レベル0のシンボルD(0番目)の数
        for symbols in symbol_list:
            symbol_count = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 音程上下考慮なし、このレベルでのシンボル数、これを簡約レベルごとに格納
            for symbol in symbols:
                symbol_count[symbol] += 1
            symbol_change.append(symbol_count)
        specific_symbol = []  # 特定のシンボルの数の遷移、二重リスト
        for i in range(len(symbol_change[0])):
            p = []
            for j in range(len(symbol_change)):
                p.append(symbol_change[j][i])
            specific_symbol.append(p)
        return specific_symbol

    """音高、音価の休符部分を削除する"""
    @staticmethod
    def reject_rest(pitch_list, duration_list, closure_pitch_key, boundary_pitch_key):
        a = []
        b = []
        c = []
        d = []
        for m in range(len(pitch_list)):
            count = 0
            norest_p = copy.copy(pitch_list[m])
            norest_d = copy.copy(duration_list[m])
            norest_closure_pitch_key = copy.copy(closure_pitch_key[m])
            norest_boundary_pitch_key = copy.copy(boundary_pitch_key[m])
            for i in range(len(norest_p)):
                if norest_p[count] == -1:
                    del norest_p[count]  # ピッチから休符を削除
                    del norest_d[count]  # durationから休符を削除
                    # del closure[count]#休符箇所に対応する部分をクロージャリストから削除
                    for k in range(len(norest_closure_pitch_key)):  # 一個休符を削除したらそれ以降のclosureを一個前に戻す
                        if norest_closure_pitch_key[k] >= count:
                            norest_closure_pitch_key[k] -= 1
                    for k in range(len(norest_boundary_pitch_key)):  # 一個休符を削除したらそれ以降のclosureを一個前に戻す
                        if norest_boundary_pitch_key[k] >= count:
                            norest_boundary_pitch_key[k] -= 1
                else:
                    count += 1
            a.append(norest_p)
            b.append(norest_d)
            c.append(norest_closure_pitch_key)
            d.append(norest_boundary_pitch_key)

        return a, b, c, d