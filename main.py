import pandas as pd
import numpy as np

from MakeIdiomSet import MakeIdiomSet
from CRFCompilerModel import CRFCompilerModel

type_array = ["gcc", "icc", "msvc", "xcode"]
makeIdiom = MakeIdiomSet()

gcc_idiom_dict = makeIdiom.directoryToIdiom("./data/gcj_text/ass/gcc/", type_array[0])
# makeIdiom.checkDict(gcc_idiom_dict)
# makeIdiom.saveIdiomDict(gcc_idiom_dict, type_array[0])
icc_idiom_dict = makeIdiom.directoryToIdiom("./data/gcj_text/ass/icc/", type_array[1])
# makeIdiom.checkDict(icc_idiom_dict)
# makeIdiom.saveIdiomDict(icc_idiom_dict, type_array[1])
msvc_idiom_dict = makeIdiom.directoryToIdiom("./data/gcj_text/ass/msvc/", type_array[2])
# makeIdiom.checkDict(msvc_idiom_dict)
# makeIdiom.saveIdiomDict(msvc_idiom_dict, type_array[2])
xcode_idiom_dict = makeIdiom.directoryToIdiom("./data/gcj_text/ass/xcode/", type_array[3])
# makeIdiom.checkDict(xcode_idiom_dict)
# makeIdiom.saveIdiomDict(xcode_idiom_dict, type_array[3])


crfModel = CRFCompilerModel()
fold = 5
target = type_array[3]
for index in range(0, fold, 1):
    print("Index : " + str(index+1))
    gcc_train, gcc_test = crfModel.kfold(gcc_idiom_dict, fold, index)
    icc_train, icc_test = crfModel.kfold(icc_idiom_dict, fold, index)
    msvc_train, msvc_test = crfModel.kfold(msvc_idiom_dict, fold, index)
    xcode_train, xcode_test = crfModel.kfold(xcode_idiom_dict, fold, index)

    train_x=[]
    train_y=[]
    test_x=[]
    test_y=[]

    train_list = None
    if(target == type_array[0]):
        train_list = gcc_train
    elif(target == type_array[1]):
        train_list = icc_train
    elif(target == type_array[2]):
        train_list = msvc_train
    elif(target == type_array[3]):
        train_list = xcode_train

    for item_dict in train_list:
        temp_x, temp_y = crfModel.dictToXY(item_dict, target)
        train_x = train_x + temp_x
        train_y = train_y + temp_y

    for item_dict in gcc_test:
        temp_x, temp_y = crfModel.dictToXY(item_dict, target)
        test_x = test_x + temp_x
        if (target == type_array[0]):
            test_y = test_y + temp_y
        else:
            for num in temp_y:
                test_y.append("0")

    for item_dict in icc_test:
        temp_x, temp_y = crfModel.dictToXY(item_dict, target)
        test_x = test_x + temp_x
        if (target == type_array[1]):
            test_y = test_y + temp_y
        else:
            for num in temp_y:
                test_y.append("0")

    for item_dict in msvc_test:
        temp_x, temp_y = crfModel.dictToXY(item_dict, target)
        test_x = test_x + temp_x
        if (target == type_array[2]):
            test_y = test_y + temp_y
        else:
            for num in temp_y:
                test_y.append("0")

    for item_dict in xcode_test:
        temp_x, temp_y = crfModel.dictToXY(item_dict, target)
        test_x = test_x + temp_x
        if (target == type_array[3]):
            test_y = test_y + temp_y
        else:
            for num in temp_y:
                test_y.append("0")

    print("====> " + target)
    print("> Train")
    crfModel.train(train_x=train_x, train_y=train_y)

    labels = crfModel.getLabels()

    print(">Test")
    crfModel.test(test_x=test_x, test_y=test_y, labels=labels)








