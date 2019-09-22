import os
import pandas as pd

class MakeIdiomSet:
    def __init__(self):
        print("Make Idiom Set")

    def directoryToIdiom(self, uri, compiler):
        dict_array=[]
        self.compiler = compiler
        try:
            self.file_list = os.listdir(uri)
            for file in self.file_list:
                dict_idiom = self.fileLoad(uri + file)
                if(dict_idiom != None):
                    dict_array.append(dict_idiom)
            return dict_array
        except IsADirectoryError | NotADirectoryError:
            print(uri + " couldn't open directory")
            return None

    def fileLoad(self, filename):
        print("File Name : " + filename)
        file_info = filename.split("/")
        self.filename = file_info[len(file_info)-1]
        self.first_dict = {}
        try:
            self.file = open(filename, 'r', encoding="utf-8")
            idiomset = self.ReadLine()
            self.file.close()
            return idiomset
        except FileNotFoundError | FileExistsError :
            print(filename + " couldn't find... please check file....")
            return None
        except EOFError:
            print(filename + " couldn't read... please check file....")
            return None

    def ReadLine(self):
        lines = self.file.readlines()
        for line in lines:
            replace_text = self.FilteringString(line)
            replace_text = self.blankProcessing(replace_text)
            # print(replace_text)
            self.splitAddressAndOp(replace_text)
        idiomset = self.sequenceDataFrame()
        return idiomset

    def blankProcessing(self, text):
        rep = text.replace("                ", " ")
        rep = rep.replace("      ", " ")
        rep = rep.replace("     ", " ")
        rep = rep.replace("    ", " ")
        rep = rep.replace("   ", " ")
        rep = rep.replace("  ", " ")
        return rep

    def FilteringString(self, text):
        if(";" in text):
            s_text = text.split(";")
            return s_text[0]+"\n"
        elif("align" in text):
            return text+"\n"
        else:
            return text

    def splitAddressAndOp(self, line):
        text = line.replace("\n", "").replace("\t", "")
        s_text = text.split(" ")
        ops = ""
        for index in range(1, len(s_text), 1) :
            ops += s_text[index]
            if(index < len(s_text)):
                ops+=" "

        if(ops == " " or ops == ""):
            ops = "None"

        s_index = s_text[0].split(":")

        # print("index : " + s_index[1] + " / ops : " + ops)
        if(s_index[1] in self.first_dict):
            arr = self.first_dict.get(s_index[1])
            arr.append(ops)
            self.first_dict.update({s_index[1]: arr})
        else:
            self.first_dict.update({s_index[1]: [ops]})

    def sequenceDataFrame(self):
        space_type = [] # gap/entry
        start_offset_point = []
        d_code_array = []

        for key in self.first_dict:
            start_offset_point.append(key)

        for item in self.first_dict.items():
            if(item[1][0] == "None"):
                space_type.append("gap")
            else:
                space_type.append("entry")

        for index in start_offset_point:
            d_code_array.append(self.first_dict.get(index))

        first_dataframe = pd.DataFrame({"type":space_type, "start_point":start_offset_point,
                                        "d_code" : d_code_array})
        # print(first_dataframe.head(25))
        idiomset = self.setIdiomList(d_code_array)
        return idiomset

    def setIdiomList(self, op_list):
        total_op_list = []
        total_idiom_dict = {}
        for ops in op_list:
            for op in ops:
                if(op=="None"):
                    continue
                total_op_list.append(op)

        total_size = len(total_op_list)
        for index in range(0, total_size-2, 1):
            pre_op_code = total_op_list[index]
            pro_op_code = total_op_list[index+2]
            idiom = pre_op_code + " | * | " + pro_op_code

            if("=" in pre_op_code):
                pre_label = "data"
            else :
                pre_label = self.compiler

            if("=" in pro_op_code):
                pro_label = "data"
            else:
                pro_label = self.compiler

            if(pre_label == pro_label):
                # print(idiom)
                # print(pre_label)

                if(total_idiom_dict.get(idiom)):
                    # Exist
                    # print("Already exist idiom. : " + idiom)
                    label = total_idiom_dict.get(idiom)[0]
                    cnt = total_idiom_dict.get(idiom)[1]+1
                    total_idiom_dict.update({idiom:[label, cnt]})
                else:
                    total_idiom_dict.update({idiom:[pre_label, 1]})
        return total_idiom_dict

    def checkDict(self, dict_list):
        index = 0
        for dict in dict_list:
            index = index + 1
            print("====> GCC Idiom file : " + str(index))
            for key in dict:
                print("Idiom : " + key)
                print("> " + str(dict.get(key)))

    def saveIdiomDict(self, dict_list, type):
        index = 0
        for dict in dict_list:
            index = index + 1
            filename = type+"_idiom_"+str(index)+".csv"
            idioms = []
            labels = []
            cnts = []
            for key in dict:
                idioms.append(key)
                labels.append(dict.get(key)[0])
                cnts.append(dict.get(key)[1])

            idiom_frame = pd.DataFrame({"idiom": idioms, "label": labels, "count": cnts})

            idiom_frame.to_csv("./data/idiom/" + filename , encoding="utf-8", index=False)
