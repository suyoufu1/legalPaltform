# -*- coding: utf-8 -*-
from sqlalchemy import or_,and_
from flask import  request, render_template, session, Blueprint
from app.models import session
from app.algorithm.KeyInfoExtraction.abstract_textrank import AbstarctTextrank
from app.utils.es_search import search_keyword,search_court,search_show
from app.utils.get_page import get_page
# 创建蓝本对象
search = Blueprint('searchs',__name__)

@search.route('/search/', methods=['GET'])
def search1():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 7))
    paginate = session.query.order_by('year').paginate(page, per_page, error_out=False)
    stus = paginate.items
    return render_template('searchShow.html',paginate=paginate,stus=stus)


@search.route('/search/keyword/', methods=['POST', 'GET'])
def keyword():
    keyword = request.form['keyword']
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 7))
    re = session.query.filter(session.keyword.like('%'+ keyword +'%'))
    paginate = session.query.filter(session.keyword.like('%'+ keyword +'%')).paginate(page, per_page, error_out=False)

    stus = paginate.items
    return render_template('searchShow2.html', paginate=paginate,stus=stus,keyword = keyword)

@search.route('/search/<court>/',endpoint="court" ,methods=['POST', 'GET'])
def court(court, page=None):
    result = search_court(court)
    age = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 7))
    paginate = session.query.filter(or_(session.documenttype.like('%'+court+'%'), session.region.like('%'+court+'%'),  session.year == court,session.keyword.like('%'+court+'%'))).paginate(page, per_page, error_out=False)
    stus = paginate.items
    parm = court
    return render_template('searchShow3.html',paginate=paginate,stus = stus,parm = parm)


@search.route('/search/show/<title>', methods=['POST', 'GET'])
def title(title):
    result1 = search_show(title)
    result = []
    for list in result1:
        result=list
        break
    # # 创建 摘要信息 对象
    abstracter = AbstarctTextrank()
    # 通过算法获得摘要信息
    keysentences = abstracter.extract_abstract(result["text"], 2)
    return render_template('show.html', result=result,keysentences = keysentences)