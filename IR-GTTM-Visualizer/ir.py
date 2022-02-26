"""
URL: Github
Author: Kaede Noto
Date: 2021/10/10
"""


# coding: utf-8

# %%
class IR_converter():
    threshold = 0
    switch = 0
    count = 0

    def IR(self, interval1, interval2, threshold=6):
        tone1 = 60
        tone2 = 60 + interval1
        tone3 = 60 + interval1 + interval2
        up = (tone2 - tone1)
        self.threshold = threshold

        P_w = self._pitch_width(tone1, tone2, tone3, self.threshold)
        S_d = self._same_direction(tone1, tone2, tone3)
        pid = self._PID(tone1, tone2, tone3, self.threshold)
        prd = self._PRD(tone1, tone2, tone3, self.threshold)

        """
        シンボル対応表
        D: 0
        P:1
        R:2 
        IP:3
        VP:4
        IR: 5, 
        VR: 6, 
        ID: 7,  
        other: 8
                """

        pattern = "NO"
        if (P_w == "00" and S_d == "yes" and pid == "yes" and prd == "yes"):
            return 0  # "D"

        elif (P_w == "SS(=)" and S_d == "no" and pid == "yes" and prd == "no"):
            if (up > 0):  # ID
                return 7
            else:
                return 7

        elif (P_w == "SS" or P_w == "SS(=)"):
            if (S_d == "yes" and pid == "yes" and prd == "yes"):
                if (up > 0):  # P
                    return 1
                elif (up < 0):
                    return 1

            elif (S_d == "no" and pid == "yes" and prd == "no"):
                if (up >= 0):  # IP
                    return 3
                elif (up <= 0):
                    return 3
        elif (P_w == "SL" and S_d == "yes" and pid == "no" and prd == "yes"):
            if (up > 0):  # VP
                return 4
            elif (up < 0):
                return 4
        elif (P_w == "SL" and S_d == "no" and pid == "no" and prd == "no"):
            # return 8#15 #"-"
            return self._reccuresive(interval1, interval2, self.threshold)
        elif (P_w == "LS" and S_d == "yes" and pid == "yes" and prd == "no"):
            if (up > 0):  # IR
                return 5
            elif (up < 0):
                return 5

        elif (P_w == "LS" and S_d == "no" and pid == "yes" and prd == "yes"):
            if (up > 0):  # R
                return 2
            elif (up < 0):
                return 2

        elif (P_w == "LL" and S_d == "yes" and pid == "no" and prd == "no"):
            # return 8#15 #"-"
            return self._reccuresive(interval1, interval2, self.threshold)
        elif (P_w == "LL" and S_d == "no" and pid == "no" and prd == "yes"):
            if (up > 0):  # VR
                return 6
            elif (up < 0):
                return 6

        if (P_w == "SL" and S_d == "no" and pid == "no" and prd == "no"):
            return self._reccuresive(interval1, interval2, self.threshold)  # 8#15 #"-"
        elif (P_w == "LL" and S_d == "yes" and pid == "no" and prd == "not"):
            return self._reccuresive(interval1, interval2, self.threshold)  # 8#15 #"-"
        else:
            return self._reccuresive(interval1, interval2, self.threshold)

    def _reccuresive(self, interval1, interval2, threshold):
        # print(tone_list[1]- tone_list[0], tone_list[2]-tone_list[1])
        if (self.switch == 0):
            threshold = 0
            self.switch = 1

        if (self.threshold < 50):
            # print("========", threshold)
            tmp = self.IR(interval1, interval2, threshold + 1)
            # print(tmp)
        else:
            tmp = 8  # ここがシンボルなし
        self.switch = 0
        return tmp  # 8#15 #"?"

    # Return L or S
    def _ReturnLorS(self, tone1, tone2, threshold):
        if (abs(tone1 - tone2) == 0):
            return 0
        if (abs(tone1 - tone2) >= threshold):
            return "L"
        if (abs(tone1 - tone2) < threshold):
            return "S"
        return "OTHER"

    # 同方向
    def _same_direction(self, tone1, tone2, tone3):
        d1 = tone2 - tone1
        d2 = tone3 - tone2

        if (d1 == 0 and d2 == 0):
            return "yes"
        elif (d1 * d2 > 0):
            return "yes"
        else:
            return "no"

    # 音程の大きさ
    def _pitch_width(self, tone1, tone2, tone3, threshold):
        if (tone1 == tone2 and tone2 == tone3):
            return "00"
        elif (abs(tone1 - tone2) == abs(tone2 - tone3) and abs(tone1 - tone2) < threshold):
            return "SS(=)"
        elif (abs(tone1 - tone2) < threshold and abs(tone2 - tone3) < threshold):
            return "SS"
        elif (abs(tone1 - tone2) < threshold and abs(tone2 - tone3) >= threshold):
            return "SL"
        elif (abs(tone1 - tone2) >= threshold and abs(tone2 - tone3) < threshold):
            return "LS"
        elif (abs(tone1 - tone2) >= threshold and abs(tone2 - tone3) >= threshold):
            return "LL"
        else:
            return "TheOtherPattern"

    def _PID(self, tone1, tone2, tone3, threshold):
        if (self._ReturnLorS(tone1, tone2, threshold) == "S" or self._ReturnLorS(tone1, tone2, threshold) == 0):
            if (abs(abs(tone2 - tone3) - abs(tone1 - tone2)) <= 4):
                return "yes"
            else:
                # print("aaaa", abs(tone2 - tone3),  abs(tone1 - tone2))
                return "no"
        if (self._ReturnLorS(tone1, tone2, threshold) == "L" and abs(tone1 - tone2) > abs(tone2 - tone3)):
            return "yes"
        else:
            return "no"

    # 6半音のときエラーが出るかも
    def _PRD(self, tone1, tone2, tone3, threshold):
        if (self._ReturnLorS(tone1, tone2, threshold) == "S" or self._ReturnLorS(tone1, tone2, threshold) == 0):
            if (self._same_direction(tone1, tone2, tone3) == "yes"):
                return "yes"
            else:
                return "no"
        elif (self._ReturnLorS(tone1, tone2, threshold) == "L" and self._same_direction(tone1, tone2, tone3) == "no"):
            return "yes"
        else:
            return "no"

    # 実現が否定かを返す
    def RorD(self, interval1, interval2, threshold):
        pid = self._PID(0, interval1, interval1 + interval2, threshold)
        prd = self._PRD(0, interval1, interval1 + interval2, threshold)
        if pid == "yes" and prd == "yes":
            return "R"
        else:
            return "D"


"""
if __name__ == "__main__":
        ir = IR_converter()
        data = [[78, 74, 74]]#[17,16,15],[8,8,8],[8,6,8],[10,12,16], [20, 12, 8], [8, 17, 15], [8, 17, 20], [8, 17, 3]]

        for i in data:
            print (ir.IR(i))
"""

# %%