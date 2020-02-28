# -*- coding: utf-8 -*-
from flask import  request, render_template, session, Blueprint
from app.models import session
from app.algorithm.sentencesimarly.sim_simhash import SimHaming
from app.utils.es_search import search_document ,search_region,search_unio,search_sim
# 创建蓝本对象
recomment = Blueprint('recomments', __name__)



@recomment.route('/recomment', methods=['GET', 'POST'])
def like():
    return render_template('similarPage.html')


@recomment.route('/recomment/keyword', methods=['POST', 'GET'])
def Type():
    document = request.form['document']
    region = request.form['region']
    des = request.form['des']

    # 通过案件类型
    results = search_document(document)
    # 定义字典，保存id和分数
    result = search_sim(des)
    num = len(result)
    # print(result)
    if not result:
        return render_template('noSimilar.html', result=result)
    return render_template('similarShow.html', result=result,num = num)
