import os
import pandas as pd

class MakeIdiomSet:
    # MakeIdiomSet은 연속적인 input 데이터를 idiom 데이터셋 형태로 전처리하는 클래스이다.
    # Idiom 데이터셋은 단일 연속 명령(single sequence instruction)인 opcode를 n-gram의 형태로 만들어준다.
    # 다음과 같은 연속된 명령이 있을 때,
    # mov rsi, [rbp+var_640] mov rdx, [rbp+var_648] lea rax, [rbp+var_670]
    # Idiom u는 다음과 같이 정할 수 있다.
    # u = (mov rsi, [rbp+var_640]  | * | lea rax, [rbp+var_670])
    def __init__(self):
        print("\n###################################")
        print(">>Make Idiom Set")

    def directoryToIdiom(self, uri=None, compiler=None):
        # Directory 내의 Input 데이터를 연속적으로 불러들인다.
        # uri : input 데이터 경로
        # compiler : gcc, icc, xcode, msvs 중 어떤 컴파일러인지 작성되어야한다.
        if( (uri == None) or (compiler == None) ):
            print("파라미터 정보를 올바르게 작성해주세요.")
            return None
        dict_array=[]
        try:
            self.file_list = os.listdir(uri)
            for file in self.file_list:
                dict_idiom = self.fileLoad(filename=uri + file, compiler=compiler)
                if(dict_idiom != None):
                    dict_array.append(dict_idiom)
            return dict_array
        except IsADirectoryError | NotADirectoryError:
            print(uri + " couldn't open directory")
            return None

    def fileLoad(self, filename, compiler):
        # 특정 파일을 Input 데이터로 불러들인다.
        # filename : 불러들일 input 파일명
        # compiler : gcc, icc, xcode, msvs 중 어떤 컴파일러인지 작성되어야한다.
        if ((filename == None) or (compiler == None)):
            print("파라미터 정보를 올바르게 작성해주세요.")
            return None
        print("File Name : " + filename)
        file_info = filename.split("/")
        self.compiler = compiler
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
        # 특정 파일의 데이터를 한줄 씩 읽어들인다.
        # output : Idiom 데이터 세트를 Dataframe 형태로 반환한다.
        lines = self.file.readlines()
        for line in lines:
            replace_text = self.FilteringString(line)
            replace_text = self.blankProcessing(replace_text)
            self.splitAddressAndOp(replace_text)
        idiomset = self.sequenceDataFrame()
        return idiomset

    def blankProcessing(self, text):
        # input 데이터의 공백에 대한 데이터 전처리를 시행한다.
        rep = text.replace("                ", " ")
        rep = rep.replace("      ", " ")
        rep = rep.replace("     ", " ")
        rep = rep.replace("    ", " ")
        rep = rep.replace("   ", " ")
        rep = rep.replace("  ", " ")
        return rep

    def FilteringString(self, text):
        # Idiom 특징과 관계없는 텍스트 정보를 전처리한다.
        if(";" in text):
            s_text = text.split(";")
            return s_text[0]+"\n"
        elif("align" in text):
            return text+"\n"
        else:
            return text

    def splitAddressAndOp(self, line):
        # 입력된 데이터에 대하여 Hex 코드의 메모리 위치정보와 opcode 명령을 분리한다.
        # 분리된 정보는 dictionary 정보로 클래스의 first_dict에 저장되며,
        # key는 메모리 위치정보이며, value 값은 ops 정보가 저장된다.
        # ops 정보에서는 opcode 정보 또는 non-code 정보가 저장되며 non-code는 변수와 같은 정보가 포함된다.
        # 위치정보만 포함된 경우 "None"으로 처리한다.
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
        # 연속된 ops 정보를 통해 gap과 entry로 구분한다.
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

        idiomset = self.setIdiomList(d_code_array)
        return idiomset

    def setIdiomList(self, op_list):
        # 연속된 ops 정보를 통해 idiom 특징을 만든다.
        # 각 idiom은 compiler(gcc, icc, msvs, xcode) 또는 data 라벨을 부여한다.
        # data 라벨은 변수와 같은 정보만 존재하는 idiom으로 정의한다.
        # 해당 idiom 정보는 dictionary 정보로 반환한다.
        # key : idiom 정보 저장
        # value : list 형태로 저장[label, idiom 빈도수]
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
                if(total_idiom_dict.get(idiom)):
                    label = total_idiom_dict.get(idiom)[0]
                    cnt = total_idiom_dict.get(idiom)[1]+1
                    total_idiom_dict.update({idiom:[label, cnt]})
                else:
                    total_idiom_dict.update({idiom:[pre_label, 1]})
        return total_idiom_dict

    def checkDict(self, dict_list):
        # 반환된 idiom dictionary 데이터에 대하여 데이터를 확인하기 위한 함수이다.
        index = 0
        for dict in dict_list:
            index = index + 1
            print("====> GCC Idiom file : " + str(index))
            for key in dict:
                print("Idiom : " + key)
                print("> " + str(dict.get(key)))

    def saveIdiomDict(self, dict_list, type, save_url):
        # 반환된 idiom dictionary 데이터를 csv 파일로 저장하기 위한 함수이다.
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

            idiom_frame.to_csv(save_url + filename , encoding="utf-8", index=False)
