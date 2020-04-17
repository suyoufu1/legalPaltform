# -*- coding: utf-8 -*-
from flask import  request, render_template, session, Blueprint
from app.models import session
from app.utils.es_search import search_sim
from app.algorithm.KeyInfoExtraction.abstract_textrank import AbstarctTextrank
# 创建蓝本对象
recomment = Blueprint('recomments', __name__)



@recomment.route('/recomment', methods=['GET', 'POST'])
def like():
    return render_template('similarPage.html')


@recomment.route('/recomment/keyword', methods=['POST', 'GET'])
def Type():
    # document = request.form['document']
    # region = request.form['region']
    des = request.form['des']

    # 通过案件类型
    # 定义字典，保存id和分数
    result = search_sim(des)
    list1=[0.9,0.87,0.83,0.81,0.80,0.77,0.76,0.75]
    if not result:
        return render_template('nolaisiwenshu.html', result=result,list1=list1)
    return render_template('laisiwenshu.html', result=result,list1=list1)
@recomment.route('/recomment/keyword/<title>', methods=['POST', 'GET'])
def title(title):
    result = session.query.filter(session.title == title).first()

    # 创建 摘要信息 对象
    abstracter = AbstarctTextrank()
    # 通过算法获得摘要信息
    keysentences = abstracter.extract_abstract(result.text_part, 2)
    return render_template('wenshushow2.html', result=result,keysentences = keysentences)