import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial
from IR_GTTM_Analyzer.converter import Converter

class Visual():
    number = 0 #今どの曲が選択されているか
    mode = 0 #現在の表示モード
    melody_list = []
    root = tk.Tk()

    def __init__(self, melody_list):
        # GUIの生成
        #self.root = tk.Tk()
        self.number = 0
        self.mode = 0
        self.root.title("IR-GTTM-Visualizer")
        self.melody_list = melody_list
        self.music_list = [str(i) for i in range(len(melody_list))]

        self.main_fig = plt.figure(figsize=(10, 8))
        self.main_ax1 = self.main_fig.add_subplot(2, 1, 1)
        self.main_ax2 = self.main_fig.add_subplot(2, 1, 2)
        # メインウィンドウのキャンバスの生成
        self.main_Canvas = FigureCanvasTkAgg(self.main_fig, master=self.root)
        self.main_Canvas.get_tk_widget().grid(row=0, column=0, rowspan=10)

        """楽曲を選択するドロップダウンリスト(これは統一してもよい？)"""
        # music_list = songTitle_s#とりあえず先頭10個にしたい
        self.var_option_music = tk.StringVar(value=self.music_list[0])  # 選択している楽曲名、初期値(value)は0番目
        self.music_option = tk.OptionMenu(self.root, self.var_option_music, *self.music_list)
        self.music_option.grid(row=0, column=1)

        """簡約レベルを選択するドロップダウンリスト、初期状態 更新の度に再設定でいける？"""
        self.MAX_REDUCTION_LEVEL = len(self.melody_list[0].reduction_melodies)  # 初期状態var_option_level.get()#differenceの要素数？
        self.reduction_list = []#選択肢用のリスト
        for i in range(self.MAX_REDUCTION_LEVEL):# 簡約レベルの数だけ選択肢を作成→これがあるせいで固定できない→mainの更新があるから可能では？→リスト内包表記を使えそう
            s = "Level: " + str(i)
            self.reduction_list.append(s)
        self.var_option_level = tk.StringVar(value=self.reduction_list[0])  # これが現在選択しているレベル、初期値は0番目
        self.reduction_option = tk.OptionMenu(self.root, self.var_option_level, *self.reduction_list)
        self.reduction_option.grid(row=0, column=2)

        # 更新ボタン
        self.ReDrawButton = tk.Button(text="更新", width=15,
                                 command = partial(self.main_window)) # ボタンの生成
        self.ReDrawButton.grid(row=2, column=1, columnspan=2)  # 描画位置

        # GTTM情報量を表示するようにモードを切り替える モード1(上グラフをGTTM情報量,下グラフをIR情報量にする)
        self.BackButton = tk.Button(text="モード切替", width=15, command=partial(self.change_mode))  # ボタンの生成
        self.BackButton.grid(row=3, column=1, columnspan=2)  # 描画位置

        # 閉じるボタン
        self.QuitButton = tk.Button(text="閉じる", width=15, command=self.Quit)  # ボタンの生成
        self.QuitButton.grid(row=4, column=1, columnspan=2)  # 描画位置

        # サブウィンドウを生成し、選択されている簡約レベルに伴いサブウィンドウに音高差分グラフを表示するボタン
        self.IRButton = tk.Button(text="音高差分表示", width=15, command=partial(self.sub_window))  # ボタンの生成
        self.IRButton.grid(row=1, column=2, columnspan=2)  # 描画位置

        self.main_window()
        self.root.mainloop()  # 描画し続ける

    """メインウィンドウ（二つのモードが存在）"""
    def main_window(self):
        """前の描画データの消去　楽曲変更やモード変更による更新用"""
        self.main_ax1.cla()
        self.main_ax2.cla()

        """現在の楽曲の情報を取得し設定"""
        self.number = self.var_option_music.get()

        """簡約レベルを選択するドロップダウンリストを更新、初期状態 更新の度に再設定でいける？"""
        self.max_redction_level = len(self.melody_list[int(self.number)].reduction_melodies)
        self.reduction_list = []
        for i in range(self.max_redction_level):
            s = "Level: " + str(i)
            self.reduction_list.append(s)
        self.var_option_level = tk.StringVar(value=self.reduction_list[0])  # これが選択しているレベル、初期値は0番目
        self.reduction_option = tk.OptionMenu(self.root, self.var_option_level, *self.reduction_list)
        self.reduction_option.grid(row=0, column=2)


        """モードに合わせて描写"""
        if self.mode == 0:
            print("現在のモード: 0  ", "現在の選択曲: ", self.number)
            specific_symbol = Converter.get_symbol_transition(self.melody_list[int(self.number)].symbol_list)
            # print(specific_symbol)
            symbol_color = ['#000000', '#e41a1c', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#377eb8', '#ff81bf',
                     "#285700"]
            symbol_label = ["D", "P", "R", "IP", "VP", "IR", "VR", "ID", "X"]
            for i in range(8):
                self.main_ax1.plot(specific_symbol[i], color=symbol_color[i], label=symbol_label[i])

            self.main_ax1.set_xlabel("Reduction Level")
            self.main_ax1.set_ylabel("Number of symbols")
            self.main_ax1.set_title(self.var_option_music.get())
            self.main_ax1.legend(loc=2)  # スペース的に右上がよさそう

            # 下のグラフ(IR情報量)
            self.main_ax2.set_xlabel("Reduction Level")
            self.main_ax2.set_ylabel("Entropy")
            self.main_ax2.plot(self.melody_list[int(self.number)].IR_entropy, color="black", marker="D", markersize=6,
                               markeredgewidth=2, markeredgecolor="blue",
                               markerfacecolor="lightblue")
            print(self.melody_list[int(self.number)].IR_entropy)

            self.main_Canvas.draw()  # キャンバスの描画

        else:
            print("現在のモード: 1")

            self.main_ax1.cla()
            self.main_ax2.cla()

            self.main_ax1.set_xlabel("Reduction Level")
            self.main_ax1.set_ylabel("Entropy(GTTM)")
            self.main_ax1.set_title(self.var_option_music.get())
            self.main_ax1.plot(self.melody_list[int(self.number)].GTTM_entropy, color="black", marker="D", markersize=6 ,markeredgewidth=2, markeredgecolor="red",
                     markerfacecolor="lightcoral")

            # 下のグラフ(IR情報量)
            self.main_ax2.set_xlabel("Reduction Level")
            self.main_ax2.set_ylabel("Entropy(IR)")
            # self.main_ax2.set_title("Entropy(GTTM + IR)")
            self.main_ax2.plot(self.melody_list[int(self.number)].IR_entropy, color="black", marker="D", markersize=6, markeredgewidth=2, markeredgecolor="blue",
                     markerfacecolor="lightblue")

            self.main_Canvas.draw()


    def sub_window(self):
        YMAX = 20
        YMIN = -20
        # 押された時点での楽曲名を取得する必要がある
        print("曲名", self.var_option_music.get())
        music_name = self.var_option_music.get()

        Lv = self.var_option_level.get()
        reduction_level = self.reduction_list.index(Lv)

        # 選択されている楽曲のデータ
        chosen_difference = self.melody_list[int(self.number)].pitch_difference[reduction_level]
        chosen_symbol_name_list = self.melody_list[int(self.number)].symbol_name_list[reduction_level]
        chosen_boundary = self.melody_list[int(self.number)].boundary
        chosen_closure = self.melody_list[int(self.number)].closure

        # closure位置のindexをまとめたリストを作成
        chosen_closure_index = []
        for i, c in enumerate(chosen_closure):
            if c >= 1:
                chosen_closure_index.append(i)

        """新たなウィンドウを作成"""
        sub = tk.Toplevel(bg="black")
        sub.title("Pitch_difference")
        # sub.geometry("300x100")
        fig = plt.figure(figsize=(11.0, 7.0))
        ax1 = fig.add_subplot()

        sub_Canvas = FigureCanvasTkAgg(fig, master=sub)
        sub_Canvas.get_tk_widget().grid(row=0, column=0, rowspan=10)  # キャンバスの座標モードをgridに?

        """音高差分を可視化する"""
        # original(元旋律)を作成する
        original = [0] * len(chosen_difference)
        ax1.plot(original, color="darkgray")

        p1 = ax1.plot(chosen_difference, marker="o", markersize=4, markeredgewidth=2, markeredgecolor="black",
                      markerfacecolor="black", color="black")  # '#696969'
        level = ": Level_" + str(reduction_level)
        f_name = str(self.number) + level  # 関数化するうえで此処が問題

        ax1.set_title(f_name)
        ax1.set_xlabel("Pitch Event")  # Timeにするには音価を使用する必要がある
        ax1.set_ylabel("Pitch difference")

        ax1.set_ylim(YMIN, YMAX)
        ax1.legend(loc=2)

        # 1. GPRBoundaryを赤い線で分割、closureよりも短く
        for i, b in enumerate(chosen_boundary):  # boundaryが存在する場合だけ赤い線を引く
            if b >= 1:
                ax1.vlines(x=i, ymax=YMAX / 3 + b * 2, ymin=YMIN / 3 - b * 2, color="red",
                           linewidth=2 + b)
        # 2. closureを青い線で分割
        for i, c in enumerate(chosen_closure):  # クロージャが存在する場合だけ青い線を引く
            if c >= 1:
                ax1.vlines(x=i, ymax=YMAX, ymin=YMIN, color="blue", linewidth=1)


        """シンボル名をグラフに表示する"""
        for t in range(len(chosen_difference) - 2):
            # もしもXだった場合表示しないシンボルの種類で色分け
            color_name = ""
            if chosen_symbol_name_list[t] != "X":
                # print(symbol_list[t])
                if chosen_symbol_name_list[t] == "D":  # D
                    color_name = '#000000'
                elif chosen_symbol_name_list[t] == "P":  # P
                    color_name = '#e41a1c'
                elif chosen_symbol_name_list[t] == "R":  # R
                    color_name = '#4daf4a'
                elif chosen_symbol_name_list[t] == "IP":  # IP
                    color_name = '#984ea3'
                elif chosen_symbol_name_list[t] == "VP":  # VP
                    color_name = '#ff7f00'
                elif chosen_symbol_name_list[t] == "IR":  # IR
                    color_name = '#22ff33'
                elif chosen_symbol_name_list[t] == "VR":  # VR
                    color_name = '#377eb8'
                else:  # ID#全部例外になってしまっている
                    color_name = '#ff81bf'

                # closureをまたがないようにシンボルを表示

                if chosen_closure[t] == 1 or chosen_closure[t + 1] == 1:  # クロージャに抵触しないようにシンボルを保存→一致していないからいくつかエラーが出る
                    continue

                ax1.text(t + 1, chosen_difference[t + 1] + 1, chosen_symbol_name_list[t], size=12, color=color_name,
                         horizontalalignment='center')

        sub_Canvas.draw()  # キャンバスの描画

        """サブ画面のボタンの生成・生成"""
        SCOREButton = tk.Button(sub, text="楽譜を表示(工事中)", width=15, command=partial(self.sampleb))
        SCOREButton.grid(row=0, column=1, columnspan=2)
        SOUNDButton = tk.Button(sub, text="画像として保存（工事中）", width=15, command=partial(self.sampleb))
        SOUNDButton.grid(row=1, column=1, columnspan=2)
        CHANGEButton = tk.Button(sub, text="モード切替（工事中）", width=15, command=partial(self.sampleb))  # durationモードに変更
        CHANGEButton.grid(row=2, column=1, columnspan=2)


    """更新ボタン（曲変更の際）"""
    def reload(self):
        #self.main_ax1.cla()
        #self.main_ax2.cla()
        self.main_window()

    """モード変更用→強制更新"""
    def change_mode(self):
        if self.mode == 0:
            self.mode = 1
            print("IR+GTTM情報量モードに変更")
            self.reload()
            self.main_window()
        else:
            self.mode = 0
            print("IRのみモードに変更")
            self.reload()


    # ボタンの動作確認用
    def sampleb(self, *args):
        print("サンプル")

    # メインウィンドウの完了ボタンで呼び出される
    def Quit(self):
        self.root.quit()
        self.root.destroy()  # 連動してサブウィンドウも閉じられる



