import requests
import re
from multiprocessing import Pool
import json
import csv
import pandas as pd
import os
import time
import collections
from bs4 import BeautifulSoup

def set_table1():
    print('*' * 80)
    print('----深圳交易所公司债券项目进度信息----')
    tabnum = int(input('请输入债券类别(1-全部；2-小公募；3-私募；4-ABS): \n'))
    dict_tables1 = {1: '全部', 2: '小公募', 3: '私募', 4: 'ABS'}
    return tabnum
def set_table2():
    select = int(input('请输入项目状态(1-全部；2-已受理；3-已反馈；4-已接受反馈意见；5-通过；6-不通过；7-终止): \n'))
    dict_tables2 = {1:'全部',2:'已受理',3:'已反馈',4:'已接收反馈意见',5:'通过',6:'不通过',7:'终止'}
    return dict_tables2[select]

def get_table(page,tabnum,select):
    if(select == '全部'):
        params = {
        'SHOWTYPE':'JSON',
        'CATALOGID':'xmjdxx',
        'TABKEY':'tab'+str(tabnum),
        'PAGENO':page,
        'random':0.45864175203129776
        }
    else:
        params = {
        'SHOWTYPE':'JSON',
        'CATALOGID':'xmjdxx',
        'TABKEY':'tab'+str(tabnum),
        'PAGENO':page,
        'selectXmzt':select,
        'random':0.45864175203129776
        }
    url = 'http://bond.szse.cn/api/report/ShowReport/data?'

    response = requests.get(url,params = params).text
    j = json.loads(response)
    pagecount = j[0]["metadata"]["pagecount"]
    data = j[0]["data"]
    if data == []:
        pagecount =0
        return pagecount,data
    else:
        recordcount = j[0]["metadata"]["recordcount"]
        if(page != pagecount):
            pagesize = j[0]["metadata"]["pagesize"]
        else:
            pagesize = len(data)

        for count in range(pagesize):
            soup = BeautifulSoup(data[count]["zqmc"], features='lxml')
            href = soup.a
            data[count]["href"]= href.get('a-param')
            zqmc = href.get_text()
            data[count]["zqmc"] = zqmc
        return pagecount,data

def write_header(data,stri,file_path):
    if data[1] != []:
        with open(file_path+'/'+stri, 'w', encoding='utf_8_sig', newline='') as f:
            headers = list(data[1][0].keys())
            writer = csv.writer(f)
            writer.writerow(headers)

    else:
        with open(file_path+'/'+stri, 'w', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow('The file is empty.')

def write_table(data,stri,file_path):
    if data[1] != []:
        for d in data:
            with open(file_path+'/'+stri, 'a', encoding='utf_8_sig', newline='') as f:
                w = csv.writer(f)
                w.writerow(d.values())

def file_name(tabnum,select):
    dict_tables1 = {1: '全部', 2: '小公募', 3: '私募', 4: 'ABS'}
    stri = '项目进度信息_'+ dict_tables1[tabnum]+'_'+select+'.csv'
    return stri

def main(page,tabnum,select,stri,file_path):
    data = get_table(page,tabnum,select)
    write_table(data[1],stri,file_path)

if __name__ == '__main__':
    #file_path = '/Users/jade/Desktop/pymini/file_szjys'
    file_path = input("请输入文件下载路径:\n")
    if not os.path.exists(file_path):
        os.mkdir(file_path)
        os.chdir(file_path)

    tabnum = set_table1()
    select = set_table2()
    stri = file_name(tabnum,select)
    write_header(get_table(1,tabnum,select),stri,file_path)

    pagecount = get_table(1,tabnum,select)[0]
    for page in range(1,pagecount+1):
        main(page,tabnum,select,stri,file_path)

    print('OK! The file is loaded.')
