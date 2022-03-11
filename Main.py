import pandas as pd
import datetime
import random
import os
Dict = pd.DataFrame()


def isnum(strIn):
    for i in strIn:
        if not ord("0") <= ord(i) <= ord("9"):
            return False
    return True


def show_Table():
    text = """
    ------------------English Revision-----------------------
    ---------------------------------------------------------
    >>>指令模式：
    >>>ADD WORD：向词库里面添加单词
    >>>TEST：开始测试
    >>>SHOWALL：查看所有单词
    >>>EXIT：退出程序
    $:
    """
    choose = input(text)
    while 1:
        if ("ADD" in choose and len(choose.split(" ")) == 2) or choose == 'TEST' or choose == 'EXIT' or choose == "SHOWALL":
            return choose
        else:
            choose = input("请输入正确的指令:\n$:")


def init_0():
    data = {"Word": ["hello"],
            "In_Date": ['2022-3-11'],
            "Wrong_Times": [0],
            "Chinese_Meanings": ['你好']}
    df = pd.DataFrame(data)
    df.to_excel("Dict.xlsx")


def init_1():
    global Dict
    Dict = pd.read_excel("Dict.xlsx", index_col=0)


def ADD(Word):
    global Dict
    Chinese_Meanings = input("请输入中文含义:")
    today_ = "{2}-{1}-{0}".format(datetime.date.today().day, datetime.date.today().month, datetime.date.today().year)
    dict0 = {"Word": [Word],
             "In_Date": [today_],
             "Wrong_Times": [0],
             "Chinese_Meanings": [Chinese_Meanings]}
    DF = pd.DataFrame(dict0)
    Dict = pd.concat([Dict, DF], ignore_index=True)


def TEST():
    global Dict
    Dict.sort_values(by='Wrong_Times', ascending=False, inplace=True)
    times = input("每次要测试的词汇个数：")
    while not isnum(times):
        times = input("请输入正确的数字：")
    checklist = []
    times = str(min(len(Dict), int(times)))
    for i in range(0, int(times), 1):
        checklist.append(False)
    Data = {"Word": [Dict.iloc[x, 0] for x in range(0, int(times), 1)],
            "In_Date": [Dict.iloc[x, 1] for x in range(0, int(times), 1)],
            "Wrong_Times": [Dict.iloc[x, 2] for x in range(0, int(times), 1)],
            "Chinese_Meanings": [Dict.iloc[x, 3] for x in range(0, int(times), 1)]}
    Dict.drop(index=list(range(0, int(times), 1)), inplace=True)
    while 1:
        finished = True
        for i in checklist:
            if not i:
                finished = False
        if finished:
            break
        id_ = random.randint(0, int(times) - 1)
        # print("id={}".format(id_))
        while checklist[id_]:
            id_ = random.randint(0, int(times) - 1)
        word = Data['Word'][id_]
        meanings = Data['Chinese_Meanings'][id_]
        mode = random.randint(0, 1)
        if mode == 0:
            ans = input("the meanings of {} is:".format(word))
            cnt = 0
            for i in ans:
                if i in meanings:
                    cnt = cnt + 1
            if cnt / len(meanings) > 0.7:
                print("Correct!The meanings of {} in the dictionary is {}".format(word, meanings))
                checklist[id_] = True
            else:
                print("Wrong...The meanings of {} in the dictionary is {}".format(word, meanings))
                Data["Wrong_Times"][id_] += 1
        else:
            ans = input("the expression of {} is:".format(meanings))
            if ans == word:
                print("Correct!The expression of {1} in the dictionary is {0}".format(word, meanings))
                checklist[id_] = True
            else:
                print("Wrong...The expression of {1} in the dictionary is {0}".format(word, meanings))
                Data["Wrong_Times"][id_] += 1
    Dict = pd.concat([Dict, pd.DataFrame(Data)], ignore_index=True)


def main():
    if not os.path.exists("Dict.xlsx"):
        init_0()
    init_1()
    while 1:
        choose = show_Table()
        if choose == "TEST":
            TEST()
        elif choose == "EXIT":
            break
        elif choose == "SHOWALL":
            print(Dict)
        else:
            ADD(choose.split(' ')[1])
    print("Saving New Data......")
    Dict.to_excel("Dict.xlsx")
    return 0


main()
