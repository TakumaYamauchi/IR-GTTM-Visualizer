import csv

def load_csv_i(path):
    csvfile = open(path, 'r', encoding="shift_jis")
    reader = csv.reader(csvfile, lineterminator='\n')
    load_list_s = [row for row in reader]
    load_list = []
    for i in load_list_s:
        #print(i)
        load_list.append([int(s) for s in i])#durationとsongTitleには使えない
    csvfile.close()
    return load_list

"""ファイル名を入力するとcsvを読み込みリストを返す(float型に変換)"""
def load_csv_f(path):
    csvfile = open(path, 'r', encoding="shift_jis")
    reader = csv.reader(csvfile, lineterminator='\n')
    load_list_s = [row for row in reader]
    load_list = []
    for i in load_list_s:
        #print(i)
        load_list.append([float(s) for s in i])#durationとsongTitleには使えない
    csvfile.close()
    return load_list

"""エラー発生中"""
"""ファイル名を入力するとcsvを読み込みリストを返す(文字列のまま)"""
def load_csv_s(path):
    csvfile = open(path, 'r', encoding="utf-8")#cp932 shift_jis
    reader = csv.reader(csvfile, lineterminator='\n')
    load_list_s = [row for row in reader]
    csvfile.close()
    return load_list_s