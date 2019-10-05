import os
import pandas as pd
import math

class GACompilerProvenance:
    # 각 컴파일러의 idiom 데이터 특징 중 구별에 중요한 영향을 미치는 특징을 토대로
    # Genetic Compiler Feature List 를 제작한다.
    # 이는 각 컴파일러의 일정 크기를 기반으로 연속된 list 정보를 가지며,
    # 해당 list 는 idiom 특징의 빈도수 값을 갖는다.
    def __init__(self):
        print("\n###################################")
        print("GA Compiler Provenance...")
        self.merge_dict = {}
        self.impact_dict = {}

    def mergeIdiom(self, x):
        # idiom dictionary 는 다음과 같은 형태를 갖는다.
        # [{idiom:labels},{idiom:labels}, ...]
        # 반환되는 merge dictionary 는 각 idiom이 key 값을 가지며, value 값은 리스트 형태를 갖는다.
        # value 값은 gcc, icc, msvs, xcode 순서의 idiom 빈도수를 갖는다.
        for idiom_dict in x:
            idioms = []
            labels = []
            for idiom in idiom_dict.keys():
                idioms.append(idiom)
                labels.append(idiom_dict.get(idiom))
            for index in range(0, len(idioms), 1):
                if(self.merge_dict.get(idioms[index])):
                    cnt_list = self.merge_dict.get(idioms[index])
                    if (labels[index] == "gcc"):
                        cnt_list[0] = cnt_list[0] + 1
                    elif (labels[index] == "icc"):
                        cnt_list[1] = cnt_list[1] + 1
                    elif (labels[index] == "msvc"):
                        cnt_list[2] = cnt_list[2] + 1
                    elif (labels[index] == "xcode"):
                        cnt_list[3] = cnt_list[3] + 1
                    self.merge_dict.update({idioms[index]: cnt_list})
                else:
                    cnt_list = [0, 0, 0, 0]
                    if (labels[index] == "gcc"):
                        cnt_list[0] = cnt_list[0] + 1
                    elif (labels[index] == "icc"):
                        cnt_list[1] = cnt_list[1] + 1
                    elif (labels[index] == "msvc"):
                        cnt_list[2] = cnt_list[2] + 1
                    elif (labels[index] == "xcode"):
                        cnt_list[3] = cnt_list[3] + 1
                    self.merge_dict.update({idioms[index]: cnt_list})

    def saveMergeDictData(self, filename = "merge_idiom_set.csv"):
        # merge dictionary 정보를 csv 파일로 저장한다.
        idioms = []
        gcc_cnt = []
        icc_cnt = []
        msvc_cnt = []
        xcode_cnt = []

        for key in self.merge_dict:
            idioms.append(key)
            cnt_list = self.merge_dict.get(key)
            gcc_cnt.append(cnt_list[0])
            icc_cnt.append(cnt_list[1])
            msvc_cnt.append(cnt_list[2])
            xcode_cnt.append(cnt_list[3])

        idiom_frame = pd.DataFrame({"idiom": idioms, "gcc": gcc_cnt, "icc": icc_cnt,
                                    "msvs" : msvc_cnt, "xcode":xcode_cnt})

        idiom_frame.to_csv("./data/idiom/"+filename, encoding="utf-8", index=False)

    def kfold(self, list, k, index):
        # validation을 위해 k-fold 방식을 위해 data를 train, test 로 데이터를 구분한다.
        size = len(list)
        s_size = int(size/k)
        s_array= []
        if(size % k > 0):
            flag = True
        else:
            flag = False
        for num in range(0, k, 1):
            if(num == (k-1)):
                if(flag):
                    s_array.append(list[(num * s_size):])
                else:
                    s_array.append(list[(num * s_size): ((num + 1) * s_size)])
            else:
                s_array.append(list[(num * s_size): ((num + 1) * s_size)])
        train = []
        test = []
        for num in range(0, len(s_array), 1):
            if(index == (num)):
                test = test + s_array[num]
            else:
                train = train+s_array[num]
        return train, test

    def dictToXY(self, dict, type):
        # Idiom Dictionary 로 부터 data와 label 정보로 분리한다.
        data_x = []
        data_y = []
        for key in dict.keys():
            data_x.append({key: dict.get(key)[0]})
            if (dict.get(key)[0] == type):
                data_y.append("1")
            else:
                data_y.append("0")
        return data_x, data_y

    def calcImpactIdiom(self, label_size, gcf_size):
        # 합쳐진 merge dictionary 정보를 통해 idiom 특징이 각 컴파일러에 주는 영향도를 측정한다.
        # 측정 방식은 유클리드 거리를 이용하며, 유클리드 값이 클수록 해당 해당 컴파일러에 영향도가 큼을 나타낸다.
        divide_size = int(gcf_size/label_size)

        self.gcc_impact_list = []
        self.icc_impact_list = []
        self.msvs_impact_list = []
        self.xcode_impact_list = []

        self.gcf_list = []

        for idiom in self.merge_dict:
            cnt_list = self.merge_dict.get(idiom)
            gcc_cnt = cnt_list[0]
            icc_cnt = cnt_list[1]
            msvs_cnt = cnt_list[2]
            xcode_cnt = cnt_list[3]

            gcc_impact = math.sqrt(math.pow(gcc_cnt-icc_cnt, 2) +
                                   math.pow(gcc_cnt-msvs_cnt, 2) +
                                   math.pow(gcc_cnt-xcode_cnt, 2))

            self.gcc_impact_list.append([idiom, gcc_impact])

            icc_impact = math.sqrt(math.pow(icc_cnt-gcc_cnt, 2) +
                                   math.pow(icc_cnt-msvs_cnt, 2) +
                                   math.pow(icc_cnt-xcode_cnt, 2))

            self.icc_impact_list.append([idiom, icc_impact])

            msvs_impact = math.sqrt(math.pow(msvs_cnt - gcc_cnt, 2) +
                                   math.pow(msvs_cnt - icc_cnt, 2) +
                                   math.pow(msvs_cnt - xcode_cnt, 2))

            self.msvs_impact_list.append([idiom, msvs_impact])

            xcode_impact = math.sqrt(math.pow(xcode_cnt - gcc_cnt, 2) +
                                    math.pow(xcode_cnt - icc_cnt, 2) +
                                    math.pow(xcode_cnt - msvs_cnt, 2))

            self.xcode_impact_list.append([idiom, xcode_impact])

        self.gcc_impact_list.sort(key=lambda x: x[1])
        self.gcc_impact_list.reverse()

        self.gcf_list = self.gcf_list + self.gcc_impact_list[0:divide_size]

        self.icc_impact_list.sort(key=lambda x: x[1])
        self.icc_impact_list.reverse()

        self.gcf_list = self.gcf_list + self.icc_impact_list[0:divide_size]

        self.msvs_impact_list.sort(key=lambda x: x[1])
        self.msvs_impact_list.reverse()

        self.gcf_list = self.gcf_list + self.msvs_impact_list[0:divide_size]

        self.xcode_impact_list.sort(key=lambda x: x[1])
        self.xcode_impact_list.reverse()

        self.gcf_list = self.gcf_list + self.xcode_impact_list[0:divide_size]

        return self.gcf_list

    def saveImpactIdiom(self, type, dic_url= "./data/idiom/"):
        # 영향도를 측정한 idiom 특징정보를 저장한다.
        idioms = []
        impacts = []
        if(type == "gcc"):
            for index in range(0, len(self.gcc_impact_list), 1):
                idioms.append(self.gcc_impact_list[index][0])
                impacts.append(self.gcc_impact_list[index][1])
        elif(type == "icc"):
            for index in range(0, len(self.icc_impact_list), 1):
                idioms.append(self.icc_impact_list[index][0])
                impacts.append(self.icc_impact_list[index][1])
        elif (type == "msvc"):
            for index in range(0, len(self.msvs_impact_list), 1):
                idioms.append(self.msvs_impact_list[index][0])
                impacts.append(self.msvs_impact_list[index][1])
        elif (type == "xcode"):
            for index in range(0, len(self.xcode_impact_list), 1):
                idioms.append(self.xcode_impact_list[index][0])
                impacts.append(self.xcode_impact_list[index][1])
        else:
            return
        idiom_frame = pd.DataFrame({"idiom": idioms, "impact": impacts})
        idiom_frame.to_csv(dic_url+type+"_impact.csv", encoding="utf-8", index=False)

    def makeIdiom(self, dict):
        # Genetic Algorithm 의 input 값인 염색체 정보로 변환하기 위해 이용되는 함수이다.
        idiom_dict = {}
        idioms = []
        for idiom in dict.keys():
            idioms.append(idiom)
        for index in range(0, len(idioms), 1):
            if(idiom_dict.get(idioms[index])):
                cnt = idiom_dict.get(idioms[index])
                idiom_dict.update({idioms[index]: cnt+1})
            else:
                idiom_dict.update({idioms[index]: 1})
        return idiom_dict

    def makeChromosome(self, train_data_list):
        # Genetic Algorithm 의 input 값인 염색체 정보로 변환하기 위해 이용되는 함수이다.
        chromo_list = []
        for dict in train_data_list:
            idiom_dict = self.makeIdiom(dict)
            temp_chromo = []
            for index in range(0, len(self.gcf_list), 1):
                if(idiom_dict.get(self.gcf_list[index][0])):
                    temp_chromo.append(idiom_dict.get(self.gcf_list[index][0]))
                else:
                    temp_chromo.append(0)
            chromo_list.append(temp_chromo)
        return chromo_list




