from __future__ import print_function
import numpy as np
from sklearn import datasets, linear_model

from genetic_selection import GeneticSelectionCV


def main():
    iris = datasets.load_iris()

    print("==> Iris Data")
    print(iris.data)

    print("==> Noisy Data correlate...")
    # Some noisy data not correlated
    E = np.random.uniform(0, 0.1, size=(len(iris.data), 20))
    print(E)

    print("==> data X")
    X = np.hstack((iris.data, E))
    print(X)
    print(len(X))
    print(len(X[0]))


    print("==> label y")
    y = iris.target
    print(y)
    print(len(y))

    estimator = linear_model.LogisticRegression(solver="liblinear", multi_class="ovr")

    selector = GeneticSelectionCV(estimator,
                                  cv=5,
                                  verbose=1,
                                  scoring="accuracy",
                                  max_features=5,
                                  n_population=50,
                                  crossover_proba=0.5,
                                  mutation_proba=0.2,
                                  n_generations=40,
                                  crossover_independent_proba=0.5,
                                  mutation_independent_proba=0.05,
                                  tournament_size=3,
                                  n_gen_no_change=10,
                                  caching=True,
                                  n_jobs=-1)
    selector = selector.fit(X, y)

    print("==> Selector ...")
    print(selector.support_)


if __name__ == "__main__":
    main()