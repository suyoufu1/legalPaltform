import os
import time
import json
from elasticsearch import Elasticsearch
# 连接ES
es = Elasticsearch(["127.0.0.1:9200"])
'''根据关键字进行事件的匹配查询'''
def search_keyword(value):
    query_body = {
        "query": {
            "multi_match": {
                "query": value,
                "fields": ["court", "documenttype", "year","keyword"]
            }

        }
    }
    searched = es.search(index="legalbook_datas", doc_type="legalbook_", body=query_body, size=100)
    # 输出查询到的结果
    list = []
    for da in searched["hits"]["hits"]:
        list.append(da["_source"])
    return list


#案件类型
def search_document(value):
    query_body = {
        "query": {
                "multi_match":{
                "query":value,
                    "fields":["court","documenttype","region"]
                    }
        }
    }
    searched = es.search(index="legalbook_datas", doc_type="legalbook_", body=query_body, size=100)
    list = []
    for da in searched["hits"]["hits"]:
        list.append(da["_source"])
    return list

'''根据court进行查询'''
def search_title(value):
    query_body ={
        "query": {
            "term" :{
            "title":value
        }
        }
    }
    searched = es.search(index="legalbook_datas", doc_type="legalbook_", body=query_body,size = 1000)
    list = []
    for da in searched["hits"]["hits"]:
        list.append(da["_source"])
    return list

def search_region(value):
    query_body ={
        "query": {
            "match" :{
            "region":value
        }
        }
    }
    searched = es.search(index="legalbook_datas", doc_type="legalbook_", body=query_body,size = 1000)
    list = []
    for da in searched["hits"]["hits"]:
        list.append(da["_source"])
    return list
def search_unio(value):
    query_body ={
        "query": {
            "multi_match":{
            "query":value,
            "fields":["court","documenttype"]
        }

        }

    }
    searched = es.search(index="legalbook_datas", doc_type="legalbook_", body=query_body,size = 1000)
    list = []
    for da in searched["hits"]["hits"]:
        list.append(da["_source"])
    return list
def search_sim(text):
    query_body ={
        "query": {
                    "match": {
                        "text": {
                            "query": text,
                            "minimum_should_match": "90%"
                        }
                    }
        }
    }
    searched = es.search(index="legalbook_datas", doc_type="legalbook_", body=query_body, size=6)
    list = []
    for da in searched["hits"]["hits"]:
        list.append(da["_source"])
    return list

#查询所有
def search_all():
    query_body ={
        "query": {
            "match_all": {

            }
        }
    }
    searched = es.search(index="legalbook_datas", doc_type="legalbook_", body=query_body, size=500)
    list = []
    for da in searched["hits"]["hits"]:
        list.append(da["_source"])
    return list

# 按标题查询进行显示
def search_show(value):
    query_body = {
      "query": {
        "match": {
          "title": {
            "query": value,
            "operator": "and"
          }
        }
      }
    }
    searched = es.search(index="legalbook_datas", doc_type="legalbook_", body=query_body, size=10000)
    list = []
    for da in searched["hits"]["hits"]:
        list.append(da["_source"])
    return list

'''根据court进行查询'''
def search_court(value):
    query_body ={
        "from": 0, "size": 10,
        "query": {
            "multi_match":{
            "query":value,
            "fields":["court","documenttype","year"]
            }

        }

    }
    searched = es.search(index="legalbook_datas", doc_type="legalbook_", body=query_body,size = 1000)
    list = []
    for da in searched["hits"]["hits"]:
        list.append(da["_source"])
    return list
def search_empty():
    query_body ={
        "query": {
            "bool": {
                "must": {
                    "exists": {
                        "field": "field"
                    }
                }
            }
        }

    }
    searched = es.search(index="legalbook_datas", doc_type="legalbook_", body=query_body,size = 1000)
    list = []
    for da in searched["hits"]["hits"]:
        list.append(da["_source"])
    return list
def es_nums():
    query_body = {
        "query": {
            "match_all":{

            }

        }

    }
    searched = es.count(index="legalbook_datas",  doc_type="legalbook_", body=query_body)
    # list = []
    # for da in searched["hits"]["hits"]:
    #     list.append(da["_source"])
    return searched['count']
