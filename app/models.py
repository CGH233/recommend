# coding :utf-8
from . import db


class Recommend(db.Model):
    __tablename__ = 'recommend'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    tag = db.Column(db.Integer)  # 类别
    recommend_level = db.Column(db.String(20))  # 推荐指数
    problemId = db.Column(db.String(20))  # 题目编号
    difficulty = db.Column(db.String(20))  # 题目难度
