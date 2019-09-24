import os
import pandas as pd
import sklearn_crfsuite
from sklearn_crfsuite import metrics


class CRFCompilerModel:
    def __init__(self):
        print("Make Idiom Set")

    def dictToXY(self, dict, type):
        data_x = []
        data_y = []
        for key in dict.keys():
            data_x.append({key: dict.get(key)[0]})
            if(dict.get(key)[0] == type):
                data_y.append("1")
            else:
                data_y.append("0")

        return data_x, data_y

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

    def train(self, train_x, train_y, epo=30):
        self.crfModel = sklearn_crfsuite.CRF(
            algorithm='lbfgs',
            c1=0.1,
            c2=0.1,
            max_iterations=100,
            all_possible_transitions=True
        )

        max_size = len(train_x)
        split_size = int(max_size/epo)
        if(max_size%epo > 0):
            split_size=split_size+1

        for index in range(0, split_size, 1):
            self.crfModel.fit(train_x[(index*epo):((index+1)*epo)],
                              train_y[(index*epo):((index+1)*epo)])

    def getLabels(self):
        labels = list(self.crfModel.classes_)
        return labels

    def test(self, test_x, test_y, labels, epo=30):
        max_size = len(test_x)
        split_size = int(max_size / epo)
        if (max_size % epo > 0):
            split_size = split_size + 1

        pred_y=[]
        for index in range(0, split_size, 1):
             temp_pred = self.crfModel.predict(test_x[(index*epo):((index+1)*epo)])
             pred_y= pred_y+temp_pred

        print(metrics.flat_f1_score(test_y, pred_y,
                      average='weighted', labels=labels))

        sorted_labels = sorted(
            labels,
            key=lambda name: (name[1:], name[0])
        )
        print(metrics.flat_classification_report(
            test_y, pred_y, labels=sorted_labels, digits=3
        ))