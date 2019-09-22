import os
import pandas as pd
import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
import math

class GACompilerProvenance:
    def __init__(self):
        print("GA Compiler Provenance...")
        self.merge_dict = {}
        self.impact_dict = {}

    def mergeIdiom(self, x):

        for idiom_dict in x:
            # [{idiom:labels},{idiom:labels}, ...]
            idioms = []
            labels = []
            for idiom in idiom_dict.keys():
                # print("==> Idiom")
                # print(idiom)
                # print(idiom_dict.get(idiom))
                idioms.append(idiom)
                labels.append(idiom_dict.get(idiom))

            for index in range(0, len(idioms), 1):
                if(self.merge_dict.get(idioms[index])):
                    cnt_list = self.merge_dict.get(idioms[index])
                    # print(labels[index])
                    if (labels[index] == "gcc"):
                        cnt_list[0] = cnt_list[0] + 1
                    elif (labels[index] == "icc"):
                        cnt_list[1] = cnt_list[1] + 1
                    elif (labels[index] == "msvc"):
                        cnt_list[2] = cnt_list[2] + 1
                    elif (labels[index] == "xcode"):
                        cnt_list[3] = cnt_list[3] + 1

                    # print(idioms[index])
                    # print(cnt_list)
                    # x = input("List")
                    self.merge_dict.update({idioms[index]: cnt_list})
                else:
                    # gcc, icc, msvs, xcode
                    cnt_list = [0, 0, 0, 0]
                    if (labels[index] == "gcc"):
                        cnt_list[0] = cnt_list[0] + 1
                    elif (labels[index] == "icc"):
                        cnt_list[1] = cnt_list[1] + 1
                    elif (labels[index] == "msvc"):
                        cnt_list[2] = cnt_list[2] + 1
                    elif (labels[index] == "xcode"):
                        cnt_list[3] = cnt_list[3] + 1

                    # print(idioms[index])
                    # print(cnt_list)
                    self.merge_dict.update({idioms[index]: cnt_list})


    def saveMergeDictData(self, filename = "merge_idiom_set.csv"):
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
        # 유클리디언 거리
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

    def saveImpactIdiom(self, type):
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
        idiom_frame.to_csv("./data/idiom/"+type+"_impact.csv", encoding="utf-8", index=False)


    def makeIdiom(self, dict):
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
        chromo_list = []

        for dict in train_data_list:
            idiom_dict = self.makeIdiom(dict)

            temp_chromo = []
            for index in range(0, len(self.gcf_list), 1):

                # print(self.gcf_list[index][0])
                # print(self.gcf_list[index][1])
                # print(idiom_dict.get(self.gcf_list[index][0]))
                # y=input("check : ")
                if(idiom_dict.get(self.gcf_list[index][0])):
                    temp_chromo.append(idiom_dict.get(self.gcf_list[index][0]))
                else:
                    temp_chromo.append(0)

            # print("Temp Chromo : ")
            # print(temp_chromo)
            # y=input("temp : ")

            chromo_list.append(temp_chromo)

        return chromo_list




