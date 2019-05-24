import csv
import requests
import json
import os
from bs4 import BeautifulSoup
import urllib.request
import re


def file_name(tabnum, select):
    dict_tables1 = {0: '小公募', 1: '私募', 2: 'ABS'}
    if tabnum is None:
        stri1 = "全部"
    else:
        stri1 = dict_tables1[tabnum]

    dict_tables2 = {1: "已受理", 2: "已反馈", 4: "通过", 5: "未通过", 8: "终止", 10: "已回复交易所意见"}
    if select is None:
        select = "全部"
    else:
        stri2 = dict_tables2[select]
    return '项目进度信息_' + stri1 + '_' + stri2


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("\nNew folder " + path + " is created.")

    else:
        print("\nThe folder already exists.")


def set_table1():
    print('*' * 80)
    print('----上海交易所公司债券项目进度信息----')
    tabnum = int(input('请输入债券类别(1-全部；2-小公募；3-私募；4-ABS): \n'))
    dict_tables1 = {1: None, 2: 0, 3: 1, 4: 2}
    return dict_tables1[tabnum]


def set_table2():
    select = int(input('请输入项目状态(1-全部；2-已受理；3-已反馈；4-通过；5-未通过；6-终止；7-已回复交易所意见): \n'))
    dict_tables2 = {1: None, 2: 1, 3: 2, 4: 4, 5: 5, 6: 8, 7: 10}
    return dict_tables2[select]


def read_info(file, stri):
    with open(file + '/' + stri, 'r') as csvfile:
        reader = csv.reader(csvfile)
        column = [row[13] for row in reader]
    column.remove('BOND_NUM')
    for col in column:
        col = int(col)
    return column


def general_info_print_data0(column, file0):
    for piece in column:
        # file = "/Users/jade/Desktop/learning/file_shjys"
        params = {
            'jsonCallBack': 'jsonpCallback75816954',
            'isPagination': False,
            'sqlId': 'COMMON_SSE_ZCZZQXMXXXX',
            'audit_id': piece,
            '_': 1558572531121
        }

        url = 'http://query.sse.com.cn/commonQuery.do?'
        referer = 'http://bond.sse.com.cn/bridge/information/index_detai.shtml?'
        referer = referer + 'bound_id=' + str(piece)
        try:
            response = requests.get(url, params=params, headers={'Referer': referer}).text
            response = response[22:-1]
            j = json.loads(response)

        except:
            print("\nDifficulty loading files.")
            print(response)
            continue
        contents = j['result']

        project_name = contents[0]['AUDIT_NAME']
        dict_cols = contents[0]

        file = file0 + "/" + project_name  # 创建新文件夹
        mkdir(file)
        dict_tables1 = {0: '小公募', 1: '私募', 2: 'ABS'}
        dict_tables2 = {1: "已受理",2: "已反馈", 4: "通过", 5: "未通过" ,8: "终止" ,10: "已回复交易所意见" }
        # 写入csv文件
        with open(file + "/" + project_name + '.csv', 'w', encoding='utf_8_sig', newline='') as f:
            for key in dict_cols.keys():
                if key == "BOND_TYPE":
                    dict_cols[key] = dict_tables1[dict_cols[key]]
                elif key == "AUDIT_STATUS":
                    dict_cols[key] = dict_tables2[dict_cols[key]]
                f.write("%s,%s\n" % (key, dict_cols[key]))

        params = {
            'jsonCallBack': 'jsonpCallback75816954',
            'isPagination': False,
            'sqlId': 'COMMON_SSE_ZCZZQXMXXXX_XXPLWJ_ZGSMS',
            'audit_id': piece,
            '_': 1558572531121
        }

        url = 'http://query.sse.com.cn/commonQuery.do?'
        referer = 'http://bond.sse.com.cn/bridge/information/index_detai.shtml?'
        referer = referer + 'bound_id=' + str(piece)
        try:
            response = requests.get(url, params=params, headers={'Referer': referer}).text
        except:
            print("\nDifficulty loading files.")
            continue

        response = response[22:-1]
        j = json.loads(response)
        contents = j['result']
        if (contents != []):
            file1 = file + "/" + "信息披露文件及备查文件"
            mkdir(file1)
            for content in contents:
                file_title = content['FILE_TITLE']
                file_path = content['FILE_PATH']
                file_time = content['FILE_TIME']
                file_title = re.split('[,|]', file_title)
                file_path = re.split('[,|]', file_path)
                file_time = re.split('[,|]', file_time)

                for i in range(len(file_title)):
                    file_name = file_time[i] + ":" + file_title[i]
                    print("\n**file_name is **", file_name)
                    url = 'http://static.sse.com.cn/bond' + file_path[i]
                    print("\n**url is **", url)
                    path = file1 + "/" + file_name
                    try:
                        data = urllib.request.urlopen(url).read()
                        with open(path, 'wb') as f:
                            f.write(data)
                            f.close()
                    except:
                        print("\nFail to download file.")
                        continue

        params = {
            'jsonCallBack': 'jsonpCallback75816954',
            'isPagination': False,
            'sqlId': 'COMMON_SSE_ZCZZQXMXXXX_FKXX_ALL',
            'audit_id': piece,
            '_': 1558572531121
        }

        url = 'http://query.sse.com.cn/commonQuery.do?'
        referer = 'http://bond.sse.com.cn/bridge/information/index_detai.shtml?'
        referer = referer + 'bound_id=' + str(piece)
        try:
            response = requests.get(url, params=params, headers={'Referer': referer}).text
            response = response[22:-1]
            j = json.loads(response)
        except:
            print("\nDifficulty loading files.")
            continue

        contents = j['result']
        if (contents != []):
            file2 = file + "/" + "反馈意见及回复"
            mkdir(file2)
            for content in contents:
                file_title = content['FILE_TITLE']
                file_path = content['FILE_PATH']
                file_time = content['UPD_TIME']
                file_title = re.split('[,|]', file_title)
                file_path = re.split('[,|]', file_path)
                file_time = re.split('[,|]', file_time)

                for i in range(len(file_title)):
                    file_name = file_time[i] + ":" + file_title[i]
                    print("\nfile_name is ***", file_name)
                    url = 'http://static.sse.com.cn/bond' + file_path[i]
                    print("\nurl is ***", url)
                    path = file2 + "/" + file_name
                    try:
                        data = urllib.request.urlopen(url).read()
                        with open(path, 'wb') as f:
                            f.write(data)
                            f.close()
                    except:
                        print("\nFail to download file.")
                        continue


if __name__ == '__main__':
    file = input("请输入文件下载路径:\n")
    mkdir(file)
    # file_path = '/Users/jade/Desktop/pymini/file_shjys'
    tabnum = set_table1()
    select = set_table2()
    stri = file_name(tabnum, select)
    newfile = file + '/' + stri
    mkdir(newfile)

    general_info_print_data0(read_info(file, stri+'.csv'), newfile)
    print('\nOK! The file is loaded.')
