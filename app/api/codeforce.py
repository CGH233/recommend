# coding:utf-8
import os
from . import api
from app import db
from app.models import Recommend
from flask import request
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from app.recommend import recommend


class Form(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField()


@api.route('/index/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@api.route('/search', methods=['GET', 'POST'])
def search():
    form = Form()
    if request.method == 'GET':
        return render_template('search.html', form=form)
    if request.method == 'POST':
        username = form.username.data
        page = request.args.get('page', 1, type=int)
        pagination = Recommend.query.filter_by(username=username).order_by(Recommend.tag.asc()).paginate(page,
                                                                                                          per_page=10,
                                                                                                          error_out=False)
        if not pagination.items:
            try:
                recommend.read_problems()
                recommend.read_users_ability(username)
                recommend.read_users_correct_problems(username)
                recommend.find_problems_to_be_evaluated()
                recommended_result, problems_dic = recommend.calculate_recommended_value(username)
                for i in range(0, 10):
                    db.session.execute(
                        Recommend.__table__.insert(),
                        [{"username": username,
                          "problemId": str(problem_ID),
                          "recommend_level": str(recommended_value),
                          "difficulty": str(problems_dic[problem_ID]['difficulty']),
                          "tag": i} for problem_ID, recommended_value in recommended_result[i]]
                    )
                    db.session.commit()  # 太烂了,我都要哭了
                pagination = Recommend.query.filter_by(username=username).order_by(Recommend.tag.desc()).paginate(1,
                                                                                                                  per_page=10,
                                                                                                                  error_out=False)
                print(pagination)
            except IOError:
                return render_template('error.html', username=username)
        return render_template('result.html', pagination=pagination, username=username)


@api.route('/result/<int:page>, <username>', methods=['GET', 'POST'])
def result(page=1, username=None):
    pagination = Recommend.query.filter_by(username=username).order_by(Recommend.tag.desc()).paginate(page, per_page=10,
                                                                                                      error_out=False)
    return render_template('result.html', pagination=pagination, username=username)
