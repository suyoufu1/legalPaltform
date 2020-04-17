from flask import  request, render_template, session, Blueprint
from app.models import session
from app.algorithm.sentencesimarly.sim_simhash import SimHaming
from app.algorithm.Crimeclass.crimepro import get_data
# 创建蓝本对象
predicti = Blueprint('predictions', __name__)


@predicti.route('/prediction', methods=['GET', 'POST'])
def prediction():
    return render_template("fanyi.html")

@predicti.route('/prediction/crimclass',methods=['GET', 'POST'])
def crim():
    keyword = request.form['keyword']
    print(keyword)
    label = get_data(keyword)
    print(label)
    return  render_template("fanyi.html",label = label)
