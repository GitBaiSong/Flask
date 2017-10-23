# coding:utf8
import warnings

from flask import *

warnings.filterwarnings("ignore")
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

# 首页
@app.route('/')
def index():
	return render_template('index.html')

# 文章列表
@app.route('/list')
def list():
	(db, cursor) = connectdb()
	cursor.execute("select * from post")
	posts = cursor.fetchall()
	for x in range(0, len(posts)):
		posts[x]['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(posts[x]['timestamp'])))
	closedb(db, cursor)
	return render_template('list.html',posts=posts)

# 文章内容
@app.route('/post/<post_id>')
def post(post_id):
	(db, cursor) = connectdb()
	cursor.execute("select * from post where id=%s",[post_id])
	post = cursor.fetchone()
	closedb(db, cursor)
	return render_template('post.html',post=post)

# 处理提交
@app.route('/handle', methods=['POST'])
def handle():
	data = request.form
	(db, cursor) = connectdb()
	cursor.execute("insert into post(title, content, timestamp) values(%s, %s, %s)", [data['title'],data['content'],int(time.time())])
	closedb(db, cursor)
	return redirect(url_for('list'))

if __name__ == '__main__':
	app.run(debug=True)
