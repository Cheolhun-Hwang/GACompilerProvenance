import pandas as pd
import numpy as np

from DataLoader import DataLoader

type_array = ["gcc", "icc", "msvc", "xcode"]

dl = DataLoader("ass", type_array[3])
dl.typeAndCodeDataloder()
dl.loadData()

