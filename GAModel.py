import os
import pandas as pd
import numpy as np
import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
import math
import random

class GAModel:
    def __init__(self, cross_over = 0.5, mutation = 0.05, pop_generation = 100):
        print("GA Model")
        self.cross_over = cross_over
        self.mutation = mutation
        self.pop_generation = pop_generation

    def run(self, chromo_origins):
        # K:1
        gene = 0
        chromo_size = len(chromo_origins[0])
        init_chromo = self.initFirstGene(gene_size=5, chromo_size=chromo_size)
        max_fit = 0
        optimal_gene = []
        chromos = None

        while(gene < self.pop_generation):
            print("=======================================================")
            print("> GENE : " + str(gene))

            if(gene == 0):
                chromos = init_chromo
            else:
                chromos = self.nextGene(chromos)

            self.showChromos(chromos)

            for chromo in chromos:
                fit_result = self.fitness(chromo, chromo_origins)
                if(fit_result > max_fit):
                    max_fit = fit_result
                    optimal_gene = chromo

            print("> Result : ")
            print("Max fit = " + str(max_fit))
            print("Optimal Gene = " + str(optimal_gene))
            gene = gene+1

        print("******> Final Result")
        print("Max fit = " + str(max_fit))
        print("Optimal Gene = " + str(optimal_gene))
        self.max_fit = max_fit
        self.optimal_gene = optimal_gene

    def getMaxFit(self):
        return self.max_fit

    def getOptimalGene(self):
        return self.optimal_gene

    def showChromos(self, chromos):
        print("> Chromos : ")
        for chromo in chromos:
            print(chromo)

    def initFirstGene(self, chromo_size, gene_size):
        init_chromo = []
        for i in range(0, gene_size, 1):
            init_chromo.append([])
            for j in range(0, chromo_size, 1):
                init_chromo[i].append(random.randint(0,1))
        return init_chromo

    def fitness(self, gene, origin):
        fit_result = []
        for origin_gene in origin:
            cos_sim_rate = self.cosSim(gene, origin_gene)
            fit_result.append(cos_sim_rate)

        avr = sum(fit_result) / len(fit_result)
        print("==> Fitness : " + str(avr) + ", list = " + str(fit_result))
        return avr

    def cosSim(self, list1, list2):
        from scipy import spatial
        return 1 - spatial.distance.cosine(list1, list2)

    def nextGene(self, before_gene):
        next_gene = []
        for index in range(0, len(before_gene), 1):
            if(index != (len(before_gene)-1)):
                cross_result = self.crossOver(before_gene[0], before_gene[1])
                next_gene.append(cross_result)
        return next_gene

    def crossOver(self, x1, x2):
        x1_next = []
        cut_size = int(len(x1) * self.cross_over)

        for index in range(0, cut_size, 1):
            x1_next.append(self.callMutation(x1[index]))

        for index in range(cut_size, len(x2), 1):
            x1_next.append(self.callMutation(x2[index]))

        return x1_next

    def callMutation(self, number):
        if random.random() < self.mutation:
            return number
        else:
            return random.randint(0, 1)

    def fit(self, x, y):
        for index in range(0, len(y), 1):
            if(y[index] == 0):
                # gcc
                self.gcc_chromo_feature = x[index]
            elif(y[index] == 1):
                # icc
                self.icc_chromo_feature = x[index]
            elif(y[index] == 2):
                # msvs
                self.msvs_chromo_feature = x[index]
            elif(y[index] == 3):
                # xcode
                self.xcode_chromo_feature = x[index]

    def classifyAll(self, x):
        classify_list = []
        for test in x:
            gcc_cos_sim = self.cosSim(test, self.gcc_chromo_feature)
            icc_cos_sim = self.cosSim(test, self.icc_chromo_feature)
            msvs_cos_sim = self.cosSim(test, self.msvs_chromo_feature)
            xcode_cos_sim = self.cosSim(test, self.xcode_chromo_feature)

            max_cos_sim = max([gcc_cos_sim, icc_cos_sim, msvs_cos_sim, xcode_cos_sim])
            if(gcc_cos_sim == max_cos_sim):
                classify_list.append(0)
            elif(icc_cos_sim == max_cos_sim):
                classify_list.append(1)
            elif (msvs_cos_sim == max_cos_sim):
                classify_list.append(2)
            elif (xcode_cos_sim == max_cos_sim):
                classify_list.append(3)

        return classify_list

    def classify(self, x, label):
        classify_list = []
        for test in x:
            gcc_cos_sim = self.cosSim(test, self.gcc_chromo_feature)
            icc_cos_sim = self.cosSim(test, self.icc_chromo_feature)
            msvs_cos_sim = self.cosSim(test, self.msvs_chromo_feature)
            xcode_cos_sim = self.cosSim(test, self.xcode_chromo_feature)

            max_cos_sim = max([gcc_cos_sim, icc_cos_sim, msvs_cos_sim, xcode_cos_sim])

            if(label == "gcc"):
                if(gcc_cos_sim == max_cos_sim):
                    classify_list.append(1)
                else:
                    classify_list.append(0)
            elif(label == "icc"):
                if(icc_cos_sim == max_cos_sim):
                    classify_list.append(1)
                else:
                    classify_list.append(0)
            elif (label == "msvs"):
                if (msvs_cos_sim == max_cos_sim):
                    classify_list.append(1)
                else:
                    classify_list.append(0)
            elif (label == "xcode"):
                if (xcode_cos_sim == max_cos_sim):
                    classify_list.append(1)
                else:
                    classify_list.append(0)

        return classify_list

    def evaluate(self, origin, classify):
        from sklearn.metrics import f1_score

        print("> Origin : " + str(origin))
        print("> Classify : " + str(classify))

        accuracy = f1_score(origin, classify, average='weighted', labels=np.unique(classify))
        print("F-Measure : {0:.4f}".format(accuracy))

        return accuracy



