from flask_paginate import Pagination,get_page_parameter
from flask import Flask, request, render_template, jsonify, json, send_file, make_response, session, Blueprint
from app.models import  session
# 创建蓝本对象
main = Blueprint('main', __name__)
# 主页界面
@main.route('/', methods=['POST', 'GET'])
def menu():
    return render_template('homepage.html')
