import pandas as pd
import numpy as np

from MakeIdiomSet import MakeIdiomSet

type_array = ["gcc", "icc", "msvc", "xcode"]
makeIdiom = MakeIdiomSet()

gcc_idiom_dict = makeIdiom.directoryToIdiom("./data/gcj_text/ass/gcc/", type_array[0])
makeIdiom.checkDict(gcc_idiom_dict)
makeIdiom.saveIdiomDict(gcc_idiom_dict, type_array[0])
icc_idiom_dict = makeIdiom.directoryToIdiom("./data/gcj_text/ass/icc/", type_array[1])
makeIdiom.checkDict(icc_idiom_dict)
makeIdiom.saveIdiomDict(icc_idiom_dict, type_array[1])
msvc_idiom_dict = makeIdiom.directoryToIdiom("./data/gcj_text/ass/msvc/", type_array[2])
makeIdiom.checkDict(msvc_idiom_dict)
makeIdiom.saveIdiomDict(msvc_idiom_dict, type_array[2])
xcode_idiom_dict = makeIdiom.directoryToIdiom("./data/gcj_text/ass/xcode/", type_array[3])
makeIdiom.checkDict(xcode_idiom_dict)
makeIdiom.saveIdiomDict(xcode_idiom_dict, type_array[3])


