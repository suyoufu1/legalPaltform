from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pymysql
import time

# 连接ES
es = Elasticsearch(
    ['47.106.183.183'],
    port=9200
)

# 连接MySQL
print("Connect to mysql...")
mysql_db = "test"
m_conn = pymysql.connect('47.106.183.183', 'root', '520000ww', 'legalbook')
m_cursor = m_conn.cursor()

try:
    num_id = 1011
    while True:
        s = time.time()
        # 查询数据
        sql = "select title, region,court,documenttype , year,information_people,text_part,referee_part,keyword from legal_instrument "
        # 这里假设查询出来的结果为 张三 26 北京
        m_cursor.execute(sql)
        query_results = m_cursor.fetchall()
        # print(str(query_results))
        if not query_results:
            print("MySQL查询结果为空 num_id=<{}>".format(num_id))
            break
        else:
            print("============")
            actions = []
            i = 0
            for line in query_results:
            # 拼接插入数据结构
                action = {
                    "_index": "legalbook_data",
                    "_type": "legalbook_",
                    "_id":i,
                    "_source": {
                        "title": line[0],
                        "region": line[1],
                        "court": line[2],
                        "documenttype": line[3],
                        "year": line[4],
                        "information": line[5],
                        "text": line[6],
                        "referee": line[7],
                        "keyword": line[8]
                    }
                }
                # 形成一个长度与查询结果数量相等的列表
                actions.append(action)
                i+=1
            # 批量插入
            a = helpers.bulk(es, actions)
            e = time.time()
            print("{} {}s".format(a, e-s))
        num_id += 1

finally:
    m_cursor.close()
    m_conn.close()
    print("MySQL connection close...")