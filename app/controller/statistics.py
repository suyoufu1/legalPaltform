# -*- coding: utf-8 -*-
from sqlalchemy import or_,and_
from flask import  request, render_template, session, Blueprint
from app.models import session
from app.algorithm.KeyInfoExtraction.abstract_textrank import AbstarctTextrank
from app.utils.es_search import search_keyword,search_all,search_document
from sqlalchemy import text
from sqlalchemy import or_,and_
from sqlalchemy.sql.expression import func
from flask_sqlalchemy  import SQLAlchemy
from flask_paginate import Pagination,get_page_parameter
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from io import BytesIO
import pymysql
import random
import jieba
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from collections import Counter
# from scipy.misc import imread
import jieba.analyse as analyse
from wordcloud import WordCloud
import numpy as np
import  time
from  app.algorithm.IdealWordCloudKit.create_cloud import CreateWordCloud


import threading
# 创建蓝本对象
statistic = Blueprint('statistics',__name__)
# 法律案情统计分析 : dstatistic
@statistic.route('/dstatistic',methods=['GET', 'POST'])
def count():
    list = search_all()
    Court = []
    Region = []
    document_Type = []
    for l in list:
        Court.append(l['court'])
        Region.append(l["region"])
        document_Type.append(l["documenttype"])
    sum11 = len(document_Type)
    # 解决中文标题乱码
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    print(document_Type)
    number = np.arange(5)
    for document in document_Type:
        # print(document)
        # 刑事裁定书
        if document == "刑事判决书":
            number[0] +=1

        # 刑事判决书
        if document== "刑事判决书":
            number[1] +=1
        # 执行裁定书
        if document == "执行裁定书":
            number[2] +=1
        # 民事
        if document == "民事判决书" or document == "刑事附带民事判决书":
            number[3] +=1
        else:
            number[4] += 1

    plt.style.use("ggplot")
    # 定义饼状图的标签
    label = '民事判决书', '刑事裁定书', '执行裁定书', '刑事判决书', '其他'
    # 记录每一个饼状图的比例
    #   print(number[0])
    size = [number[3] / 100, number[0] / 100, number[2] / 100, number[1] / 100, number[4] / 100]
    # 定义每一块的颜色
    colors = ['yellow', 'lightskyblue', 'lightcoral', 'green', 'blue']

    plt.pie(size, labels=label, colors=colors, autopct='%1.1f%%', shadow=True, startangle=110)
    plt.title('案件类型比例图 总数量:' + str(sum11))
    plt.axis('equal')
    #   print(sum)
    plt.savefig("app/static/" + "案件类型统计2.jpg")
    #   plt.show()
    return render_template('statistics.html', court=Court, region=Region, document_Type=document_Type)

# 关键字搜索statistics
@statistic.route('/dstatistic/<DT>',endpoint="DT", methods=['POST', 'GET'])
def DT(DT):
    results = search_document(DT)
    # results = session.query.filter(DT == session.document_Type).all()
    # print(results[0].title)
    if not results:
        return render_template('worldcloudStatistics.html')
    # 定义一个字符串，保存关键字
    keyword = ""
    for res in results:
        keyword += str(res["keyword"])
    # 分词
    fe = '|'.join(jieba.cut(keyword))
    santi_words = [x for x in jieba.cut(fe) if len(x) >= 0]
    jieba.disable_parallel()
    # 提取关键字
    c = Counter(santi_words).most_common(1000)
    keys = ""
    for word in c:
        if word[0].isdigit():
            del word
        else:
            keys += str(word)
    # 词云制作
    font = 'app/static/HYQiHei-55J.ttf'  # 选择字体路径，这里使用了黑体G:/pythonWeb/web/005.jpg
    color_mask = plt.imread("app/static/keyword/china.jpg")  # 读取模板图片，这里使用了一张五角星图片
    cloud = WordCloud(font_path=font, background_color='white', mask=color_mask, max_words=200, max_font_size=200,
                      width=3000, height=3000, random_state=42)  # 设置词云参数，字体，模板，背景白色，最大词量100个，最大字体尺寸100
    # word_cloud = cloud.generate(fe)
    cloud.generate(fe)
    # 基于彩色图像生成相应彩色
    image_colors = ImageColorGenerator(color_mask)
    plt.imshow(cloud)
    # 关闭坐标轴
    plt.axis('off')
    # 绘制词云
    plt.figure()
    plt.imshow(cloud.recolor(color_func=image_colors))
    plt.axis('off')
    # 保存图片
    word_cloud2 = cloud.generate(str(keys))  # 产生词云数据 word_cloud
    # wcould="分词词云_"
    wcould2 = "词云"
    img = wcould2 + ".jpg"
    l = 'app/static/keyword/'
    word_cloud2.to_file(l + '/' + img)
    cloud.to_file(l + '/' + 'cloudword.png')
    return render_template('worldcloudStatistics.html',  val1=time.time())
# 涉案人员统计 ：info
@statistic.route('/dstatistic/info',methods=['POST','GET'])
def keyword1():

      keyword=request.form['keyword1']
      print(keyword)
      list = search_keyword(keyword)
      number = np.arange(6)
      for l in list:
          # print(document)
          # 刑事裁定书
          if l["documenttype"] == "刑事判决书":
              number[0] += 1

          # 刑事判决书
          if l["documenttype"] == "刑事判决书":
              number[1] += 1
          # 执行裁定书
          if l["documenttype"] == "执行裁定书":
              number[2] += 1
          # 民事
          if l["documenttype"] == "民事判决书" :
              number[3] += 1
          if  l["documenttype"] == "刑事附带民事判决书":
              number[4] += 1
      # 解决中文标题乱码
      plt.rcParams['font.sans-serif'] = ['SimHei']
      plt.rcParams['axes.unicode_minus'] = False
      font = {'family' : 'sans-serif','weight' : 'normal','size' : 23}
    #   print (plt.style.available)
      plt.style.use("ggplot")
      # 创建一个点数为 8 x 6 的窗口, 并设置分辨率为 80像素/每英寸
      plt.figure(figsize=(25, 20), dpi=500)
      # 再创建一个规格为 1 x 1 的子图
      plt.subplot(1, 1, 1)
      # 柱子总数
      N = 6
      # 包含每个柱子对应值的序列
      values = number
      # 包含每个柱子下标的序列
      index = np.arange(N)
      # 柱子的宽度
      width = 0.35
      # 绘制柱状图, 每根柱子的颜色为紫罗兰色
      p2 = plt.bar(index, values, tick_label=number,label="rainfall",color="#87CEFA")
      # 设置横轴标签
      plt.xlabel("案件类型",font)
      # 设置纵轴标签
      plt.ylabel('数量 (个)',font)
      # 添加标题
      plt.title('"'+keyword+'"'+"所对应的案件类型数量直方图",fontsize=50,color="purple")
      # 添加纵横轴的刻度
      plt.xticks(index, ('民事判决书', '执行裁定书', '刑事裁定书', '刑事判决书', '刑事附带民事裁定书'),fontsize="16")
      plt.yticks(np.arange(0, max(number)+5, int((max(number)+5)/10+1)),fontsize=23)
      '''
      for rect in p2: 
            height = rect.get_height() 
            plt.text(rect.get_x() + rect.get_width() / 2, height+1, str(height), ha="center", va="bottom",size=20)
      '''
      # 添加图例
      plt.savefig("app/static/统计/"+"统计.jpg")
      return render_template('keywordStatistics.html',val1=time.time())

