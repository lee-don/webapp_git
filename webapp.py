import os

from flask import Flask, request,render_template, send_from_directory,session,redirect,url_for
from Forms import *
from tools.common.cm import *
from tools.goe_forecast.zzm import *
from tools.geo.atti import Atti
from tools.common.My_Mail import My_Mail

mail = My_Mail()



app = Flask(__name__)
# app.config.from_object(Config)
app.debug = True

app.config["SECRET_KEY"] = "123456"  # 或者 app.secret_key = '123456'




@app.route('/')
def home():
    return render_template('index.html')

@app.route("/down2")
def down1():
    print('down1')
    return send_from_directory(r"./templates/",filename="lc004.zip",as_attachment=True)



@app.route('/sendmailto',methods=['post'])
def sendmailto():
    sendto = request.args.get('sendto',type=str,default=None)
    title = request.args.get('title', type=str, default=None)
    content = request.args.get('content', type=str, default=None)
    mail.send_mail(sendto,title,content,'xx')
    return 'suc'



@app.route('/sendmail',methods=['post'])
def sendmail():
    name = request.form.get('name',type=str,default=None)
    email = request.form.get('email', type=str, default=None)
    message = request.form.get('message', type=str, default=None)
    content = '联系人:' +name+ '\n' +'电子邮件:' +email+ '\n' +'建议：\n' +message+ '' 
    mail.send_mail('835046414@qq.com','建议意见-[' + name + ']-来自系统',content,'xx')
    return 'suc'


@app.route('/kaipiaoxingxi')
def kaipiaoxingxi():
    return render_template('kaipiaoxingxi.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def login_inter(acc,pas):
    suc = True
    session['token'] = get_a_uuid()
    return suc

def logout_inter():
    session['token'] = None

def url_forlogin():
    if session.get('token') == None:
        return (True,redirect(url_for('login')))
    else:
        return (False,None)


#登陆及登录后主页
@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    logout_inter()
    if form.validate_on_submit():
        session['name'] = form.acc.data
        session['password'] = form.password.data
        if login_inter(form.acc.data,form.password.data):
            return redirect(url_for('main'))
    return render_template('login.html', form=form)

@app.route('/main')
def main():
    if session.get('token') == None:
        return redirect(url_for('login'))
    return render_template('main.html',noon=whatnoon(),name=session.get('name'))

# 上报表单
@app.route('/dayly',methods=['GET', 'POST'])
def dayly():
    result=url_forlogin()
    if result[0]:
        return result[1]
    form = DaylyForm()
    if form.validate_on_submit():
        if login_inter(form.acc.data,form.password.data):
            return redirect(url_for('user'))
    return render_template('dayly.html', form=form)







from tools.common.QRcode import get_qrcode
# get_qrcode
@app.route('/qrcode',methods=['POST','GET'])
def qrcode():
    try:
        words = request.args.get('words', type=str, default='http://www.baidu.com')
        f = get_qrcode(words)
        (file_path, file_name) = os.path.split(f)
        return send_from_directory(file_path, file_name, as_attachment=True)
    except Exception:
        return 'Exception'





# 掌子面分级接口 localhost/zzmlevel?rc=较软岩&kv=破碎&is_fault=&water=喷出&crustal_stress=高地应力
@app.route('/zzmlevel',methods=['POST','GET'])
def zzm():
    rc_d_or_s = request.args.get('rc',type=str,default=None)
    kv_d_or_s = request.args.get('kv', type=str, default=None)
    is_fault  = request.args.get('is_fault', type=bool, default=False)
    water_d_or_s = request.args.get('water', type=str, default=None)
    crustal_stress_str = request.args.get('crustal_stress', type=str, default=None)
    zzm=Zzm(rc_d_or_s,kv_d_or_s,is_fault,water_d_or_s,crustal_stress_str)
    return obj_to_result_json(zzm.zzmResult)


# 产状接口
@app.route('/att_strs',methods=['POST','GET'])
def att_strs():
    att_str = request.args.get('att_str',type=str,default=None)
    att=Atti.get_a_Atti_from_str(att_str).get_Attstrs()
    return obj_to_result_json(att)

@app.route('/view_angle',methods=['POST','GET'])
def view_angle():
    att_str = request.args.get('att_str',type=str,default=None)
    section_dir = request.args.get('section_dir', type=float, default=None)
    att=Atti.get_a_Atti_from_str(att_str)
    beta = att.cal_view_angle(section_dir)
    return to_result_json(beta)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


