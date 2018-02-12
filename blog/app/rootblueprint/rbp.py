from flask import Blueprint,session,render_template,redirect,url_for,current_app,request
from blog.app.db_models import Role,User
from blog.app.form import Login_Form
from blog.app.factory import db
from blog.app.email_fun import send_email
rootbp=Blueprint('root_bp',__name__,template_folder='root_bp_templates',static_folder='root_bp_static')

@rootbp.route('/')
def index():
    return render_template('index.html')


@rootbp.route('/t',methods=['GET','POST'])
def test():
    if request.form.get('name'):
        session['namee']=request.form.get('name')
        return render_template('ff.html',namee=request.form.get('name'))
        # return redirect(url_for('.jump'))
    return render_template('t.html')


@rootbp.route('/jump',methods=['GET','POST'])
def jump():
    if request.form.get('first'):
        return render_template('t.html',name=request.form.get('first'))
    return render_template('ff.html')