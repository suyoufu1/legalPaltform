from flask import  request, render_template, session, Blueprint
from app.models import session
from app.algorithm.sentencesimarly.sim_simhash import SimHaming
# 创建蓝本对象
predicti = Blueprint('predictions', __name__)


@predicti.route('/prediction', methods=['GET', 'POST'])
def prediction():
    return render_template("crimepage.html")

@predicti.route('/prediction/crimclass',methods=['GET', 'POST'])
def crim():
    keyword = request.form['keyword']
    print(keyword)
    while (1):
        sent = input(keyword)
    return  render_template("crimeclass.html",label = label)
