# DataLoader : Assembly file을 입력받고 데이터를 정제하는 Class
import os
import pandas as pd

class DataLoader:
    def __init__(self, type=None, code=None):
        print("Data Loader class init")
        self.type = type
        self.code = code

    def fileLoad(self, filename):
        print("File Name : " + filename)
        file_info = filename.split("/")
        self.filename = file_info[len(file_info)-1]
        self.first_dict = {}
        self.hexSetting()
        try:
            self.file = open(filename, 'r', encoding="utf-8")
            self.ReadLine()
            self.file.close()
        except FileNotFoundError | FileExistsError :
            print(filename + " couldn't find... please check file....")
        except EOFError:
            print(filename + " couldn't read... please check file....")

    def DirectoryLoad(self, pathname):
        print("Directory : " + pathname)
        try:
            self.file_list = os.listdir(pathname)
            for file in self.file_list:
                self.fileLoad(pathname+file)
                # Break Point
                # x = input("다음 파일 진행 : ")

        except IsADirectoryError | NotADirectoryError:
            print(pathname + " couldn't open directory")

    def loadData(self):
        self.DirectoryLoad(self.data_url)

    def typeAndCodeDataloder(self):
        data_url = "./data/gcj_text/"
        if(self.type == "ass"):
            data_url+="ass/"
        elif(self.type == "hex"):
            data_url+="hex/"
        else:
            print("잘못된 타입 정보 입니다.")
            return

        if(self.code == "gcc"):
            data_url+="gcc/"
        elif(self.code == "icc"):
            data_url+="icc/"
        elif(self.code == "msvc"):
            data_url+="msvc/"
        elif(self.code == "xcode"):
            data_url+="xcode/"
        else:
            print("잘못된 코드 정보 입니다.")
            return

        print("경로 설정 완료")
        print("uri : " + data_url)
        self.data_url = data_url

    def ReadLine(self):
        lines = self.file.readlines()
        for line in lines:
            replace_text = self.FilteringString(line)
            replace_text = self.blankProcessing(replace_text)
            print(replace_text)
            self.firstProcessing(replace_text)

        for key, item in self.first_dict.items():
            res = "key = {key}, value={value}".format(key=key, value=item)
            print(res)
            self.SaveData(self.filename, res+"\n")
        self.secondProcessing()

    def hexSetting(self):
        try:
            self.hex_dict = {}
            hex_file = open("./data/gcj_text/hex/"+self.code+"/"+self.filename, 'r', encoding="utf-8")
            lines = hex_file.readlines()
            hex_file.close()
            for line in lines:
                s_hex = line.replace("\ufeff", "").replace(" \n", "").split("  ", 1)
                arr = []
                arr.append(s_hex[1][0:2])
                arr.append(s_hex[1][3:5])
                arr.append(s_hex[1][6:8])
                arr.append(s_hex[1][9:11])
                arr.append(s_hex[1][12:14])
                arr.append(s_hex[1][15:17])
                arr.append(s_hex[1][18:20])
                arr.append(s_hex[1][21:23])
                arr.append(s_hex[1][25:27])
                arr.append(s_hex[1][28:30])
                arr.append(s_hex[1][31:33])
                arr.append(s_hex[1][34:36])
                arr.append(s_hex[1][37:39])
                arr.append(s_hex[1][40:42])
                arr.append(s_hex[1][43:45])
                arr.append(s_hex[1][46:48])
                self.hex_dict.update({s_hex[0] : arr})

        except FileNotFoundError | FileExistsError :
            print("couldn't find... please check file....")
        except EOFError:
            print("couldn't read... please check file....")

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

    def firstProcessing(self, line):
        text = line.replace("\n", "").replace("\t", "")
        print("origin : " + text)
        s_text = text.split(" ")
        print("leng : " + str(len(s_text)))
        ops = ""
        for index in range(1, len(s_text), 1) :
            ops += s_text[index]
            if(index < len(s_text)):
                ops+=" "

        if(ops == " " or ops == ""):
            ops = "None"

        s_index = s_text[0].split(":")

        print("index : " + s_index[1] + " / ops : " + ops)
        if(s_index[1] in self.first_dict):
            arr = self.first_dict.get(s_index[1])
            arr.append(ops)
            self.first_dict.update({s_index[1]: arr})
        else:
            self.first_dict.update({s_index[1]: [ops]})

    def secondProcessing(self):
        space_type = [] # gap/entry
        start_offset_point = []
        end_offset_point = []
        hex_offset = []
        d_code_array = []

        for key in self.first_dict:
            start_offset_point.append(key)
        for index in range(1, len(start_offset_point)):
            end_offset_point.append(start_offset_point[index])
        end_offset_point.append("None")

        for item in self.first_dict.items():
            if(item[1][0] == "None"):
                space_type.append("gap")
            else:
                space_type.append("entry")

        for index in range(0, len(start_offset_point), 1):
            print(space_type[index] + " / " + start_offset_point[index] + " / " + end_offset_point[index])
            hex_return_array = self.returnHexAray(start_offset_point[index], end_offset_point[index])
            hex_offset.append(hex_return_array)

        for index in start_offset_point:
            d_code_array.append(self.first_dict.get(index))

        first_dataframe = pd.DataFrame({"type":space_type, "start_point":start_offset_point,
                                        "end_point":end_offset_point, "hex_code":hex_offset,
                                        "d_code" : d_code_array})

        print(first_dataframe.head(25))

        first_dataframe.to_csv("./data/result/"+self.filename+"_first_processing_data.csv", encoding="utf-8", index=False)

    def returnHexAray(self, start, end):
        if(end == "None"):
            return None
        print("start : " + start + " / end : " + end)
        start_index_ten = start[0:len(start)-1]
        end_index_ten = end[0: len(end) - 1]
        print("start : " + start_index_ten + " / end : " + end_index_ten)

        if( (start_index_ten + "0") == (end_index_ten + "0") ):
            hex_arr = self.hex_dict.get(start_index_ten + "0")
            print(hex_arr)
            arr = []
            # if (hex_arr == None):
            #     print("No Hex Dictionary... ")
            #     return arr
            start_int = self.getIndex(start)
            end_int = self.getIndex(end)
            for num in range(start_int, 16, 1):
                if num == end_int:
                    break
                arr.append(hex_arr[num])
            print(arr)
            return arr
        else:
            start_int_ten = self.getIndex(start_index_ten)
            start_int = self.getIndex(start)
            end_int_ten = self.getIndex(end_index_ten)
            end_int = self.getIndex(end)
            print("start_int_ten : " + str(start_int_ten))
            print("end_int_ten : " + str(end_int_ten))
            print("start int : " + str(start_int))
            print("end int : " + str(end_int))

            dif_size_tem = end_int_ten - start_int_ten
            print("DIF SIZE : " + str(dif_size_tem))
            arr = []
            if( dif_size_tem > 1 ):
                start_index_hundred = self.getIndex(start[0:len(start) - 2])
                end_index_hundred = self.getIndex(end[0: len(end) - 2])
                print("Start Hundred : " + start[0:len(start) - 2])
                print("End Hundred : " + end[0: len(end) - 2])
                dif_size_hundred = end_index_hundred - start_index_hundred
                if( dif_size_hundred > 1):
                    # 백의 자리 이상의 차이
                    print("Digit : over 100")
                    start_int_hundred = self.getIndex(str(start_index_hundred))
                    end_int_hundred = self.getIndex(str(end_index_hundred))

                    # Start
                    hex_arr = self.hex_dict.get(start_index_ten + "0")
                    print(hex_arr)
                    for num in range(start_int, 16, 1):
                        arr.append(hex_arr[num])

                    # Middle
                    middle_index_array = []
                    for h in range(start_int_hundred + 1, end_int_hundred, 1):
                        for t in range(0, 16, 1):
                            middle_index_array.append(start[0:len(start) - 3] + self.getHex(h) + self.getHex(t) + "0")
                    for hex_code in range(0, len(middle_index_array), 1):
                        print("Middle Hex Code : " + str(hex_code))
                        hex_arr = self.hex_dict.get(str(hex_code))
                        if(hex_arr == None):
                            print("No Hex Dictionary... ")
                            break
                        print(hex_arr)
                        for num in range(0, 16, 1):
                            arr.append(hex_arr[num])
                    # End
                    hex_arr = self.hex_dict.get(end_index_ten + "0")
                    print(hex_arr)
                    for num in range(0, end_int, 1):
                        arr.append(hex_arr[num])

                    x = input("Please Handle it...")
                else :
                    # 십의 자리까지의 차이
                    print("Digit : 10")
                    start_int_ten = self.getIndex(start_index_ten)
                    end_int_ten = self.getIndex(end_index_ten)
                    print("start index ten : " + str(start_int_ten))
                    print("end index ten : " + str(end_int_ten))
                    # Start
                    hex_arr = self.hex_dict.get(start_index_ten + "0")
                    print(hex_arr)
                    for num in range(start_int, 16, 1):
                        arr.append(hex_arr[num])

                    # Middle
                    middle_index_array = []
                    for num in range(start_int_ten+1, end_int_ten, 1):
                        middle_index_array.append(start[0:len(start) - 2]+self.getHex(num)+"0")
                    print(middle_index_array)

                    for hex_code in range(0, len(middle_index_array), 1):
                        print("Middle Hex Code : " + str(hex_code))
                        hex_arr = self.hex_dict.get(str(hex_code))
                        if(hex_arr == None):
                            print("No Hex Dictionary... ")
                            break
                        print(hex_arr)
                        for num in range(0, 16, 1):
                            arr.append(hex_arr[num])

                    # End
                    hex_arr = self.hex_dict.get(end_index_ten + "0")
                    print(hex_arr)
                    for num in range(0, end_int, 1):
                        arr.append(hex_arr[num])

                    print(arr)
            else:
                # Start
                hex_arr = self.hex_dict.get(start_index_ten + "0")
                print(hex_arr)
                for num in range(start_int, 16, 1):
                    arr.append(hex_arr[num])

                # End
                hex_arr = self.hex_dict.get(end_index_ten + "0")
                print(hex_arr)
                for num in range(0, end_int, 1):
                    arr.append(hex_arr[num])

                print(arr)
            return arr



    def getIndex(self, text):
        last_string = text[len(text)-1:len(text)]
        if(last_string == "0"):
            return 0
        elif(last_string == "1"):
            return 1
        elif (last_string == "2"):
            return 2
        elif (last_string == "3"):
            return 3
        elif (last_string == "4"):
            return 4
        elif (last_string == "5"):
            return 5
        elif (last_string == "6"):
            return 6
        elif (last_string == "7"):
            return 7
        elif (last_string == "8"):
            return 8
        elif (last_string == "9"):
            return 9
        elif (last_string == "A"):
            return 10
        elif (last_string == "B"):
            return 11
        elif (last_string == "C"):
            return 12
        elif (last_string == "D"):
            return 13
        elif (last_string == "E"):
            return 14
        elif (last_string == "F"):
            return 15

    def getHex(self, num):
        if(num == 0):
            return "0"
        elif(num == 1):
            return "1"
        elif (num == 2):
            return "2"
        elif (num == 3):
            return "3"
        elif (num == 4):
            return "4"
        elif (num == 5):
            return "5"
        elif (num == 6):
            return "6"
        elif (num == 7):
            return "7"
        elif (num == 8):
            return "8"
        elif (num == 9):
            return "9"
        elif (num == 10):
            return "A"
        elif (num == 11):
            return "B"
        elif (num == 12):
            return "C"
        elif (num == 13):
            return "D"
        elif (num == 14):
            return "E"
        elif (num == 15):
            return "F"

    def SaveData(self, filename, line):
        saveFile = open("data/result/" + filename, mode='a', encoding="utf-8")
        saveFile.write(line)
        saveFile.close()