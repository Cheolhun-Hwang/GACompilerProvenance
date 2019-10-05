from MakeIdiomSet import MakeIdiomSet
from CRFCompilerModel import CRFCompilerModel
from GACompilerProvenance import GACompilerProvenance
from GAModel import GAModel
from GeneticModel import GeneticModel

def runCRFModel(target = None, fold = 5):
    if target == None:
        print("input 정보를 확인해주세요.")
        return
    crfModel = CRFCompilerModel()
    for index in range(0, fold, 1):
        print("k-fold : " + str(index + 1))
        gcc_train, gcc_test = crfModel.kfold(dict=gcc_idiom_dict, k=fold, index=index)
        icc_train, icc_test = crfModel.kfold(dict=icc_idiom_dict, k=fold, index=index)
        msvc_train, msvc_test = crfModel.kfold(dict=msvc_idiom_dict, k=fold, index=index)
        xcode_train, xcode_test = crfModel.kfold(dict=xcode_idiom_dict, k=fold, index=index)

        train_x = []
        train_y = []
        test_x = []
        test_y = []

        train_list = None
        if (target == type_array[0]):
            train_list = gcc_train
        elif (target == type_array[1]):
            train_list = icc_train
        elif (target == type_array[2]):
            train_list = msvc_train
        elif (target == type_array[3]):
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

def runGAModel(gcf_define_size=256, fold = 5):
    final_total = []
    final_gcc=[]
    final_icc=[]
    final_msvs=[]
    final_xcode=[]

    for index in range(0, fold, 1):
        print("k-fold : " + str(index + 1))
        gaModel = GACompilerProvenance()

        gcc_train, gcc_test = gaModel.kfold(gcc_idiom_dict, fold, index)
        icc_train, icc_test = gaModel.kfold(icc_idiom_dict, fold, index)
        msvc_train, msvc_test = gaModel.kfold(msvc_idiom_dict, fold, index)
        xcode_train, xcode_test = gaModel.kfold(xcode_idiom_dict, fold, index)

        train_x = []
        train_y = []

        for item_dict in gcc_train:
            temp_x, temp_y = gaModel.dictToXY(item_dict, gcc_train)
            train_x = train_x + temp_x
            train_y = train_y + temp_y

        for item_dict in icc_train:
            temp_x, temp_y = gaModel.dictToXY(item_dict, icc_train)
            train_x = train_x + temp_x
            train_y = train_y + temp_y

        for item_dict in msvc_train:
            temp_x, temp_y = gaModel.dictToXY(item_dict, msvc_train)
            train_x = train_x + temp_x
            train_y = train_y + temp_y

        for item_dict in xcode_train:
            temp_x, temp_y = gaModel.dictToXY(item_dict, xcode_train)
            train_x = train_x + temp_x
            train_y = train_y + temp_y

        gaModel.mergeIdiom(train_x)
        # gaModel.saveMergeDictData("merge_idiom_set_" + str(index) + ".csv")
        chrom_feature_list = gaModel.calcImpactIdiom(label_size=4, gcf_size=gcf_define_size)
        print(chrom_feature_list)

        # gaModel.saveImpactIdiom("gcc")
        # gaModel.saveImpactIdiom("icc")
        # gaModel.saveImpactIdiom("msvc")
        # gaModel.saveImpactIdiom("xcode")

        # model = GAModel()
        model = GeneticModel()

        print("==> Chromos.... GCC")
        gcc_chromosome = gaModel.makeChromosome(gcc_train)
        model.run(gcc_chromosome, 100)
        gcc_max_fit = model.getMaxFit()
        gcc_optimal_chromo = model.getOptimalGene()

        print("==> Chromos.... ICC")
        icc_chromosome = gaModel.makeChromosome(icc_train)
        model.run(icc_chromosome, 100)
        icc_max_fit = model.getMaxFit()
        icc_optimal_chromo = model.getOptimalGene()

        print("==> Chromos.... MSVS")
        msvs_chromosome = gaModel.makeChromosome(msvc_train)
        model.run(msvs_chromosome, 100)
        msvs_max_fit = model.getMaxFit()
        msvs_optimal_chromo = model.getOptimalGene()

        print("==> Chromos.... Xcode")
        xcode_chromosome = gaModel.makeChromosome(xcode_train)
        model.run(xcode_chromosome, 100)
        xcode_max_fit = model.getMaxFit()
        xcode_optimal_chromo = model.getOptimalGene()

        model.fit(x=[gcc_optimal_chromo, icc_optimal_chromo, msvs_optimal_chromo, xcode_optimal_chromo],
                  y=[0, 1, 2, 3])

        print("==> Test : ")
        gcc_label_test = []
        icc_label_test = []
        msvs_label_test = []
        xcode_label_test = []
        total_label_test = []

        print("==> Chromos.... GCC")
        gcc_chromosome_test = gaModel.makeChromosome(gcc_test)
        for chromo in gcc_chromosome_test:
            total_label_test.append(0)
            gcc_label_test.append(1)
            icc_label_test.append(0)
            msvs_label_test.append(0)
            xcode_label_test.append(0)

        print("==> Chromos.... ICC")
        icc_chromosome_test = gaModel.makeChromosome(icc_test)
        for chromo in icc_chromosome_test:
            total_label_test.append(1)
            gcc_label_test.append(0)
            icc_label_test.append(1)
            msvs_label_test.append(0)
            xcode_label_test.append(0)

        print("==> Chromos.... MSVS")
        msvs_chromosome_test = gaModel.makeChromosome(msvc_test)
        for chromo in msvs_chromosome_test:
            total_label_test.append(2)
            gcc_label_test.append(0)
            icc_label_test.append(0)
            msvs_label_test.append(1)
            xcode_label_test.append(0)

        print("==> Chromos.... Xcode")
        xcode_chromosome_test = gaModel.makeChromosome(xcode_test)
        for chromo in xcode_chromosome_test:
            total_label_test.append(3)
            gcc_label_test.append(0)
            icc_label_test.append(0)
            msvs_label_test.append(0)
            xcode_label_test.append(1)

        test_chromo_x = gcc_chromosome_test + icc_chromosome_test + msvs_chromosome_test + \
                        xcode_chromosome_test

        classify_total_y = model.classifyAll(x=test_chromo_x)
        classify_gcc_y = model.classify(x=gcc_label_test, label="gcc")
        classify_icc_y = model.classify(x=icc_label_test, label="icc")
        classify_msvs_y = model.classify(x=msvs_label_test, label="msvs")
        classify_xcode_y = model.classify(x=xcode_label_test, label="xcode")

        print("====================================================")
        print("**> Evaluate (f-measure)")
        print("> Total : ")
        total_res = model.evaluate(total_label_test, classify_total_y)
        final_total.append(total_res)
        print("> Gcc : ")
        gcc_res = model.evaluate(gcc_label_test, classify_gcc_y)
        final_gcc.append(gcc_res)
        print("> Icc : ")
        icc_res = model.evaluate(icc_label_test, classify_icc_y)
        final_icc.append(icc_res)
        print("> Msvs : ")
        msvs_res = model.evaluate(msvs_label_test, classify_msvs_y)
        final_msvs.append(msvs_res)
        print("> Xcode : ")
        xcode_res = model.evaluate(xcode_label_test, classify_xcode_y)
        final_xcode.append(xcode_res)
    print("\n====================================================")
    print("> Total : {0:.4f}".format(sum(final_total)/len(final_total)))
    print("> GCC : {0:.4f}".format(sum(final_gcc) / len(final_gcc)))
    print("> ICC : {0:.4f}".format(sum(final_icc) / len(final_icc)))
    print("> MSVS : {0:.4f}".format(sum(final_msvs) / len(final_msvs)))
    print("> Xcode : {0:.4f}".format(sum(final_xcode) / len(final_xcode)))

# Compiler Label 정의
type_array = ["gcc", "icc", "msvc", "xcode"]

# MakeIdiomSet : Input > Idiom dictionary 데이터 전처리
makeIdiom = MakeIdiomSet()

gcc_idiom_dict = makeIdiom.directoryToIdiom(uri="./data/gcj_text/ass/gcc/", compiler=type_array[0])
makeIdiom.checkDict(dict_list=gcc_idiom_dict)
makeIdiom.saveIdiomDict(save_url="./data/idiom/", dict_list=gcc_idiom_dict, type=type_array[0])

icc_idiom_dict = makeIdiom.directoryToIdiom(uri="./data/gcj_text/ass/icc/", compiler=type_array[1])
makeIdiom.checkDict(dict_list=icc_idiom_dict)
makeIdiom.saveIdiomDict(save_url="./data/idiom/", dict_list=icc_idiom_dict, type=type_array[1])

msvc_idiom_dict = makeIdiom.directoryToIdiom(uri="./data/gcj_text/ass/msvc/", compiler=type_array[2])
makeIdiom.checkDict(dict_list=msvc_idiom_dict)
makeIdiom.saveIdiomDict(save_url="./data/idiom/", dict_list=msvc_idiom_dict, type=type_array[2])

xcode_idiom_dict = makeIdiom.directoryToIdiom(uri="./data/gcj_text/ass/xcode/", compiler=type_array[3])
makeIdiom.checkDict(dict_list=xcode_idiom_dict)
makeIdiom.saveIdiomDict(save_url="./data/idiom/", dict_list=xcode_idiom_dict, type=type_array[3])

# CRF 모델을 이용한 idiom 데이터 분석
# for target in type_array:
#     runCRFModel(target=target)

# ex) ICC Compiler classifier
# runCRFModel(target=type_array[1])

# GCFL과 GA 모델을 이용한 idiom 데이터 분석
runGAModel(gcf_define_size=256)




