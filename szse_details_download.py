import csv
import requests
import json
import os
from bs4 import BeautifulSoup
import urllib.request


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("\nNew folder " + path + " is created.")

    else:
        print("\nThe folder " +path +" already exists.")


def set_table1():
    print('*' * 80)
    print('----深圳交易所公司债券项目进度信息----')
    tabnum = int(input('请输入债券类别(1-全部；2-小公募；3-私募；4-ABS): \n'))
    dict_tables1 = {1: '全部', 2: '小公募', 3: '私募', 4: 'ABS'}
    return tabnum


def set_table2():
    select = int(input('请输入项目状态(1-全部；2-已受理；3-已反馈；4-已接受反馈意见；5-通过；6-不通过；7-终止): \n'))
    dict_tables2 = {1: '全部', 2: '已受理', 3: '已反馈', 4: '已接收反馈意见', 5: '通过', 6: '不通过', 7: '终止'}
    return dict_tables2[select]


def file_name(tabnum, select):
    dict_tables1 = {1: '全部', 2: '小公募', 3: '私募', 4: 'ABS'}
    stri = '项目进度信息_' + dict_tables1[tabnum] + '_' + select
    return stri


def read_info(file, stri):
    with open(file + '/' + stri, 'r') as csvfile:
        reader = csv.reader(csvfile)
        column = [row[7] for row in reader]
    column.remove('href')
    # print(column)
    return column


def general_info_print_data0(column, file0):
    for piece in column:
        url = 'http://bond.szse.cn/api/report'
        url = url + piece
        try:
            response = requests.get(url).text
            j = json.loads(response)
            #print('\n*****'+url+'\n\n**********',j)
            #print('\n**length:',len(j))
        except:
            print("Difficulty loading files",response)

        title_name = j[0]['metadata']['name']
        dict_cols = j[0]['metadata']['cols']
        dict_data = j[0]['data'][0]
        project_name = dict_data['zqmc']

        file = file0+"/"+project_name #创建新文件夹
        mkdir(file)
        #写入csv文件
        with open( file + "/" + project_name + '.csv', 'w',encoding='utf_8_sig', newline='') as f:
            for key in dict_cols.keys():
                f.write("%s,%s,%s\n"%(key,dict_cols[key],dict_data[key]))

        if (len(j)>1):
            mjsms = j[1]['data'][0]['mjsms']

            soup = BeautifulSoup(mjsms, features='lxml')
            #print(soup)
            pdf_href= soup.a.get('encode-open')
            #print(pdf_href)
            pdf_href = 'http://reportdocs.static.szse.cn'+pdf_href
            file_name = soup.get_text()
            date = j[1]['data'][0]['mjsmsgxrq']
            print('\n**This is pdf file link**',pdf_href)
            print('\n**This is the name of pdf file**',file_name)

            url = pdf_href
            #url = 'http://static.sse.com.cn/bond/bridge/information/c/201905/79d1482a5ff645ff9ab125b2dffaea99.pdf'
            path = file +"/"+ file_name +date+".pdf"
            try:
                data = urllib.request.urlopen(url).read()
                with open(path ,'wb') as f:
                    f.write(data)
                    f.close()
            except:
                print("\nFail to download file:"+path)#still have not opened a pdf file successfully.

            fkyjh_data = j[2]['data']
            if(fkyjh_data != []):
                #print("-----------",len(fkyjh_data))
                for obj in fkyjh_data:
                    link = obj['fkyjh']
                    soup = BeautifulSoup(link, features='lxml')
                    href= soup.a.get('encode-open')
                    #print(href)
                    href = 'http://reportdocs.static.szse.cn'+href
                    file_name = soup.get_text()#获取href/file_name
                    sequence = obj['sequence']
                    data = obj['fkyjhgxrq']
                    print("\n**This is the word file downloading link**",href)
                    print("\n**This is the name of word file**",file_name)
                    path = file +"/"+ "反馈意见"+file_name +date+".doc"
                    try:
                        urllib.request.urlretrieve(href, path)
                    except:
                        print("\nFail to download file: "+path)

if __name__ == '__main__':
    file = input("请输入文件下载路径:\n")
    mkdir(file)
    tabnum = set_table1()
    select = set_table2()
    stri = file_name(tabnum, select)
    newfile = file + '/' + stri
    mkdir(newfile)
    # file = "/Users/jade/Desktop/pymini/file_szjys"
    general_info_print_data0(read_info(file, stri+'.csv'), newfile)
    print('\nOK! The file is loaded.')
