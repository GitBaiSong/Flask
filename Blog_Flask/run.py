#coding:utf8

from flask import Flask,render_template,url_for,request,redirect,session
import pymysql
import pymysql.cursors
from config import *
import time

app = Flask(__name__)
app.config.from_object(__name__)

# 连接数据库
def connectdb():
	db = pymysql.connect(host=HOST, user=USER, passwd=PASSWORD, db=DATABASE, port=PORT, charset=CHARSET, cursorclass = pymysql.cursors.DictCursor)
	db.autocommit(True)
	cursor = db.cursor()
	return (db,cursor)

# 关闭数据库
def closedb(db,cursor):
	db.close()
	cursor.close()

#博客主页
@app.route('/')
@app.route('/index')
def index():
	if 'user_id' in session:
		print("sessin 为：%s" %session.get("user_id"))
		return render_template("index.html")

	return u"You are not logged in"
	# return 

#文章列表
@app.route('/list')
def list():
	return render_template("list.html")


#用户登录
@app.route('/login',methods=["GET","POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	else:
		username = request.form.get("username")
		password = request.form.get("password")


		(db, cursor) = connectdb()

		
		cursor.execute("SELECT * FROM user WHERE username = %s",[username])
		db_user = cursor.fetchone()
		print(type(db_user))
		print(db_user)



		if username != db_user["username"]:
			return u'用户名错误！'

		elif password != db_user["password"]:
			return u'密码错误！'
		else:
			session["user_id"] = db_user["id"]
			print("session 设置为: %s" %session["user_id"])
			closedb(db, cursor)
			return redirect(url_for("index"))


#注册用户
@app.route('/register',methods=["GET","POST"])
def register():
	if request.method == 'GET':
		return render_template("register.html")

	else:
		username = request.form.get('username')
		password = request.form.get('password')
		phone = request.form.get('phone')
		email = request.form.get('email')


		(db,cursor) = connectdb()
		db_exist_username = cursor.execute("select * from user where username=%s ",[username])
		db_exist_phone = cursor.execute("select * from user where phone=%s ",[phone])
		# 用户名和手机号验证
		if db_exist_username:
			return u"该用户名已被注册，请更换用户名！"
		elif db_exist_phone:
			return u"该手机号码已被注册，请更换手机号码! "
		else:
			#新建用户
			cursor.execute("insert into user(username, password, phone, email, creat_time) values(%s, %s, %s, %s, %s)",[username, password, phone, email,int(time.time())])
			closedb(db, cursor)
			return redirect(url_for("login"))

#添加文章
@app.route('/ManageArticle',methods=["GET","POST"])
def ManageArticle():
	if 'user_id' in session:
		print("sessin 为：%s" %session.get("user_id"))
		if request.method == "GET":
			return render_template("ManageArticle.html")
		else:
			article_data = request.form
			print("用户提交的表单是%s"%article_data)
			print("用户名：%s"%article_data['title'])
			user_id = session.get('user_id')
			print("session_id = %s "%user_id)

			(db,cursor) = connectdb()

			cursor.execute("SELECT username FROM user WHERE id = %s",[user_id])
			author = cursor.fetchone()
			print("session_username=%s"%author["username"])

			cursor.execute("INSERT INTO article(title, author, content, creat_time, user_article) VALUES(%s, %s, %s, %s, %s)",[article_data['title'], author["username"],article_data['content'], int(time.time()), int(user_id)])

			cursor.execute("INSERT INTO label(label) VALUES (%s)",[article_data['label']])

			closedb(db, cursor)
			return u"添加成功"

			#return render_template(url_for(articlename(article_data['title'])))
	else:
		print(u"没有session")


#文章详情页
@app.route('/list/<articlename>',methods=['GET','POST'])
def articlename(articlename):
	return render_template("article.html")

if __name__ == "__main__":
	app.run()

