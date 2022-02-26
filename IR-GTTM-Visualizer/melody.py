"""旋律の各種情報を格納するクラス"""
import copy
from IR_GTTM_Analyzer.converter import Converter
from IR_GTTM_Analyzer.calc_entropy import CalcEntropy

class Melody():
    pitch_list = []  # 音高列
    duration_list = []  # 音価列
    symbol_list = []  # シンボル列（段階リスト）
    symbol_name_list = []  # シンボル名列
    reduction_melodies = []  # 簡約旋律
    pitch_difference = []  # 音高差分旋律
    IR_entropy = []  # 簡約レベル毎のIR情報量リスト
    GTTM_entropy = []  # 簡約レベル毎のGTTM情報量リスト
    closure = []  # closure位置
    boundary = []  # boudary位置
    rank = []
    parents = []
    title = ""

    #インスタンス生成時に自動で呼び出されるコンストラクタ
    def __init__(self, pitch, duration, closure, boundary, rank, parents):
        #self.converter3 = Converter.Converter()
        self.pitch_list = pitch
        self.duration_list = duration
        self.closure = closure
        self.boundary = boundary
        self.rank = rank
        self.parents = parents
        self.reduction_melodies = self.reduction(pitch, rank, parents)
        self.pitch_difference = self.calc_pitch_difference_list(self.reduction_melodies)
        self.IR_entropy = []
        self.symbol_list = []
        self.symbol_name_list = []
        for i in range(len(self.reduction_melodies)):
            print(i)
            self.symbol_list.append(CalcEntropy.get_symbol_list(self.pitch_difference[i], closure))
            self.symbol_name_list.append(Converter.get_symbolname_list(CalcEntropy.get_symbol_list(self.pitch_difference[i], closure)))
            self.IR_entropy.append(CalcEntropy.calc_entropy_IR(CalcEntropy.get_symbol_list(self.pitch_difference[i], closure)))
            print(CalcEntropy.calc_entropy_IR(CalcEntropy.get_symbol_list(self.pitch_difference[i], closure)))
        self.GTTM_entropy = CalcEntropy.calc_entropy_GTTM(duration, rank, parents)
        print(self.IR_entropy)
        print(self.GTTM_entropy)

        self.melody_print()

    """旋律の情報を表示"""
    def melody_print(self):
        print("旋律情報")
        print("簡約旋律:", self.reduction_melodies)
        print("音高差分:", self.pitch_difference)

    """IR情報量を取得する"""
    def getIR_Entropy(self):
        return self.IR_entropy

    """GTTM情報量を取得する"""
    def getGTTM_entropy(self):
        return self.GTTM_entropy

    """GTTM簡約を行う"""
    def reduction(self, pitch_list, rank, parents):
        reduction_melodies = []
        pitch_name_list = Converter.No2pitch_list(pitch_list)
        print("簡約レベル0(元旋律)", pitch_name_list)
        # 最大回数=(階層の数-1)回簡約
        reduction_melody = copy.copy(pitch_list)
        reduction_melodies.append(pitch_list)  # 元旋律を入れておく
        # rankからhierarchyの作成
        hierarchy = []
        for i in range(max(rank) + 1):
            layer = [j for j, v in enumerate(rank) if v == i]
            hierarchy.append(layer)
        for reductionLevel in range(len(hierarchy) - 1):
            for l in range(reductionLevel + 1):
                for i in hierarchy[reductionLevel - l]:
                    reduction_melody[i] = reduction_melody[parents[i]]
            label_name = "簡約レベル" + str(reductionLevel + 1)
            pitch_name_list = Converter.No2pitch_list(reduction_melody)
            print(label_name, pitch_name_list)
            reduction_melodies.append(copy.copy(reduction_melody))
        return reduction_melodies

    """元旋律と簡約した旋律の音高差分を計算する関数"""
    def calc_pitch_difference(self, om, rm):  # om:元旋律 rm:簡約旋律
        if len(om) != len(rm):
            print("")
        d = []
        for i in range(len(om)):
            t = om[i] - rm[i]#rm[i] - om[i]
            d.append(t)
        return d

    """簡約旋律を入れたら音高差分リストを返す関数"""
    def calc_pitch_difference_list(self, reduction_melodies):
        pitch_difference = []
        for i in range(len(reduction_melodies)):
            d = self.calc_pitch_difference(reduction_melodies[0], reduction_melodies[i])
            pitch_difference.append(d)
        return pitch_difference