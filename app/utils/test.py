#!/usr/bin/python
# coding=utf-8

# 常用参数：
# index - 索引名
# q - 查询指定匹配 使用Lucene查询语法
# from_ - 查询起始点  默认0
# doc_type - 文档类型
# size - 指定查询条数 默认10
# params - 查询的字段

import datetime
import sys
import getopt
from elasticsearch import Elasticsearch

"""
初始化elasticsearch连接
"""
def init_es():
    return Elasticsearch(["localhost:9200"])

"""
查询数据
"""
def query_data( puid, count):
    es = init_es()
    para = {"_source":"title"}
    data_array = es.search(index='legalbook_datas', q='offset: "'+ str(puid) +'"', doc_type='legalbook_' ,params=para, size=int(count))

    print_data(data_array, count)

"""
分页查询数据
"""
def query_data_by_page(log_date, puid, page_count, page_num):
    es = init_es()
    para = {"_source":"message"}
    index_name = "center-"+log_date
    from_page = int(page_count) * (int(page_num)-1)

    data_array = es.search(index=index_name, q='offset: "'+ str(puid) +'"', doc_type='doc' ,params=para, size=int(page_count), from_=from_page)

    print_data(data_array, page_count)

"""
打印数据
"""
def print_data(data_array, count):

    datas = data_array["hits"]["hits"]

    print("符合条件的数据总条数为：" + str(data_array['hits']['total']))
    print("具体内容如下：")
    for data in datas:
        print(data['_source']['message'])

"""
处理逻辑调用查询
"""
def run(param):
    puid = param['puid']
    log_date = param['log_date'] if param['log_date'] else datetime.datetime.now().strftime('%Y.%m.%d')
    count = param['count'] if param['count'] else 50
    is_page = param['is_page']

    if not is_page:
        query_data(log_date, puid, count)
    else:
        page_count = param['page_count']
        page_num = param['page_num']
        query_data_by_page(log_date, puid, page_count, page_num)

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'hp:l:c:io:n:',
                                   ['help', 'puid=', 'log_date=', 'count=', 'is_page', 'page_count=', 'page_num='])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    if not opts:
        print("The puid is a must !")
        opts = [('-h', '')]

    VARS = {'puid': None, 'log_date': None, 'count': None,'is_page': False, 'page_count': 50, 'page_num': 1}

    for opt, value in opts:

        if opt in ('-h', '--help'):
            print("")
            print("Usage：python query_client_log.py -p puid [-c count -l log_date -i [-o page_count -n page_count]] | --puid=puid ....")
            print("-p, --puid           用户id")
            print("-l, --log_date       数据日期，格式：yyyy.mm.dd")
            print("-c, --count          查询数据的条数，默认50条")
            print("-i, --is_page        用于标记是否分页, 默认不分页")
            print("-o, --page_count     分页查询，每页数据的条数，默认每页50条")
            print("-n, --page_num       分页查询，当选查询的页号，默认从第1页开始查询")
            print("-h, --help           查看帮助并退出")
            print("")
            sys.exit()

        if opt in ('-p', '--puid'):
            VARS['puid'] = value
        elif opt in ('-l', '--log_date'):
            VARS['log_date'] = value
        elif opt in ('-c', '--count'):
            VARS['count'] = value
        elif opt in ('-i', '--is_page'):
            VARS['is_page'] = True
        elif opt in ('-o', '--page_count'):
            VARS['page_count'] = value
        elif opt in ('-n', '--page_num'):
            VARS['page_num'] = value

    run(VARS)


if __name__ == '__main__':
    query_data( 10, 1000)