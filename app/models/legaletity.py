# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from app.extensions import db
class session(db.Model):
    __tablename__ = 'legal_instrument'
    ID = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(100))  # 标题
    region = db.Column(db.String(100))  # 地区
    court = db.Column(db.String(100))  # 法院
    documenttype = db.Column(db.String(100))  # 文书类型
    year = db.Column(db.String(100))  # 年份
    document_number = db.Column(db.String(100))  # 文书编号
    information_people = db.Column(db.String(100))  # 当事人
    text_part = db.Column(db.String(100))  # 正文
    referee_part = db.Column(db.String(100))  # 裁判部分
    other = db.Column(db.String(100))  # 其他
    keyword = db.Column(db.VARCHAR(300))  # 关键字
    def getMany(self):
        session.query.filter().all