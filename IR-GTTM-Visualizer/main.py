from IR_GTTM_Analyzer import csv_method
from IR_GTTM_Analyzer import melody
from IR_GTTM_Analyzer.converter import Converter
from IR_GTTM_Analyzer import visual



if __name__ == "__main__":
    try:
        """各種データをCSVファイルから読み込み"""
        pitch = csv_method.load_csv_i('music_data/pitch.csv')
        duration = csv_method.load_csv_f('music_data/duration.csv')
        parents = csv_method.load_csv_i('music_data/parents.csv')
        rank = csv_method.load_csv_i('music_data/rank.csv')
        boundary = csv_method.load_csv_i('music_data/boundary.csv')
        closure = csv_method.load_csv_i('music_data/closure.csv')

        """休符の削除処理"""
        pitch_norest, duration_norest, closure_norest, boundary_norest = Converter.reject_rest(pitch,
                                                                                               duration,
                                                                                               closure,
                                                                                               boundary)
        """Melodyインスタンスを生成してリスト化"""
        N = len(pitch_norest)
        print(N)
        melody_list = []

        for i in range(N):
            m = melody.Melody(pitch_norest[i],
                              duration_norest[i],
                              closure_norest[i],
                              boundary_norest[i],
                              rank[i],
                              parents[i])
            melody_list.append(m)

        #print("楽曲データ数: ", len(melody_list))

        visualizer = visual.Visual(melody_list)

    except:
        import traceback
        traceback.print_exc()
    finally:
        input(">>")