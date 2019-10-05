import sklearn_crfsuite
from sklearn_crfsuite import metrics


class CRFCompilerModel:
    # 선행 연구에 대한 실험 모델
    # Idiom 특징과 CRF 모델인 그래픽 확률 모델을 이용한 컴파일러 분석 모델
    # 제작던 idiom 데이터를 기반으로 구분의 목표가 되는 컴파일러를 분류하는 것을 목표로한다.
    # input : idiom dictionary, label
    # output : result
    def __init__(self):
        print("\n###################################")
        print(">>CRFCompilerModel")

    def dictToXY(self, dict, type):
        # Idiom Dictionary 로 부터 data와 label 정보로 분리한다.
        data_x = []
        data_y = []
        for key in dict.keys():
            data_x.append({key: dict.get(key)[0]})
            if(dict.get(key)[0] == type):
                data_y.append("1")
            else:
                data_y.append("0")

        return data_x, data_y

    def kfold(self, dict, k, index):
        # validation을 위해 k-fold 방식을 위해 data를 train, test 로 데이터를 구분한다.
        size = len(dict)
        s_size = int(size/k)
        s_array= []
        if(size % k > 0):
            flag = True
        else:
            flag = False
        for num in range(0, k, 1):
            if(num == (k-1)):
                if(flag):
                    s_array.append(dict[(num * s_size):])
                else:
                    s_array.append(dict[(num * s_size): ((num + 1) * s_size)])
            else:
                s_array.append(dict[(num * s_size): ((num + 1) * s_size)])
        train = []
        test = []
        for num in range(0, len(s_array), 1):
            if(index == (num)):
                test = test + s_array[num]
            else:
                train = train+s_array[num]
        return train, test

    def train(self, train_x, train_y, epo=30):
        # crf 그래픽 확률 모델을 학습한다.
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
        # 학습된 모델에서 분류한 label 정보를 반환한다.
        labels = list(self.crfModel.classes_)
        return labels

    def test(self, test_x, test_y, labels, epo=30):
        # 학습된 crf 그래픽 확률 모델을 기반으로 테스트 결과를 반환한다.
        # output : 예측 결과(list), 예측 확률(f-measure)
        max_size = len(test_x)
        split_size = int(max_size / epo)
        if (max_size % epo > 0):
            split_size = split_size + 1

        pred_y=[]
        for index in range(0, split_size, 1):
             temp_pred = self.crfModel.predict(test_x[(index*epo):((index+1)*epo)])
             pred_y= pred_y+temp_pred

        f_result = metrics.flat_f1_score(test_y, pred_y,
                      average='weighted', labels=labels)

        print(">> F-measure accuracy : " + str(f_result))

        sorted_labels = sorted(
            labels,
            key=lambda name: (name[1:], name[0])
        )
        print(metrics.flat_classification_report(test_y, pred_y, labels=sorted_labels, digits=3))
        return f_result, pred_y