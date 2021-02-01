import pymysql
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_restful import reqparse, abort, Api, Resource

# Flask api
app = Flask(__name__)
api = Api(app)

# mysql 연결하기
db = pymysql.connect(
        user = 'root',
        passwd = '1234',
        host = '127.0.0.1',
        port = 3306,
        db = 'board-service',
        charset = 'utf8'
    )
cursor = db.cursor()

# parser 변수를 통해 클라이언트로부터 전달 받는 인자들을 지정
parser = reqparse.RequestParser()
parser.add_argument("id")
parser.add_argument("name")

class Board(Resource):
    # 현재 등록된 게시판 정보 조회
    def get(self):
        sql = "SELECT id, name FROM `board`"
        cursor.execute(sql)
        result = cursor.fetchall()
        return jsonify(status = "success", result = result)
    
    # name을 입력받아 새로운 게시판 생성
    def post(self):
        args = parser.parse_args()
        sql = "INSERT INTO `board` (`name`) VALUES (%s)"
        cursor.execute(sql, (args['name']))
        db.commit()
        
        return jsonify(status = "success", result = {"name": args["name"]})
    
    # 기존 게시판의 name을 변경
    def put(self):
        args = parser.parse_args()
        sql = "UPDATE `board` SET name = %s WHERE `id` = %s"
        cursor.execute(sql, (args['name'], args["id"]))
        db.commit()
        
        return jsonify(status = "success", result = {"id": args["id"], "name": args["name"]})
    
    # 게시판의 id를 입력받아 제거
    def delete(self):
        args = parser.parse_args()
        sql = "DELETE FROM `board` WHERE `id` = %s"
        cursor.execute(sql, (args["id"]))
        db.commit()
        
        return jsonify(status = "success", result = {"id": args["id"]})

parser.add_argument("id")
parser.add_argument("title")
parser.add_argument("content")
parser.add_argument("board_id")

class BoardArticle(Resource):

    # 글 조회하기
    def get(self, board_id=None, board_article_id=None):
        if board_article_id:
            sql = "SELECT `id`, `title`, `content` FROM `boardArticle` WHERE `id`=%s"
            cursor.execute(sql, (board_article_id,))
            result = cursor.fetchone()
        else:
            sql = "SELECT `id`, `title`, `content` FROM `boardArticle` WHERE `board_id`=%s"
            cursor.execute(sql, (board_id,))
            result = cursor.fetchall()
            
        return jsonify(status = "success", result = result)

    # 글 작성하기
    def post(self, board_id=None):
        args = parser.parse_args()
        sql = "INSERT INTO `boardArticle` (`title`, `content`, `board_id`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (args['title'], args['content'], args['board_id']))
        db.commit()
        
        return jsonify(status = "success", result = {"title": args["title"]})
        
    # 글 수정하기
    def put(self, board_id=None, board_article_id=None):
        args = parser.parse_args()
        sql = "UPDATE `boardArticle` SET `title` = %s, `content` = %s WHERE `id` = %s"
        cursor.execute(sql, (args['title'], args["content"], args["id"]))
        db.commit()
        
        return jsonify(status = "success", result = {"title": args["title"], "content": args["content"]})
        
    # 글 삭제하기
    def delete(self, board_id=None, board_article_id=None):
        args = parser.parse_args()
        sql = "DELETE FROM `boardArticle` WHERE `id` = %s"
        cursor.execute(sql, (args["id"], ))
        db.commit()
        
        return jsonify(status = "success", result = {"id": args["id"]})

parser.add_argument("num")

class Dashboard(Resource):

    # 각각의 게시판의 가장 최근 n(=5)개의 글의 title을 조회하기
    def get(self, num=None):
        sql = "SELECT * FROM ( SELECT *, RANK() OVER (PARTITION BY `board_id` ORDER BY `create_date` DESC) AS `RN` FROM `boardarticle` AS `M` ) AS `topscore` WHERE `topscore`.`RN` <= %s"
        cursor.execute(sql, (args["num"]))
        result = cursor.fetchall()

        return jsonify(status = "success", result = result)

# User APIs
app.config.from_mapping(SECRET_KEY='dev')

@app.route('/')
@app.route('/auth/login', methods =['GET', 'POST']) 
def login(): 
    if request.method == 'POST': 
        fullname = request.form['email'] 
        password = request.form['password'] 
        sql = "SELECT * FROM `user` WHERE `email`=%s AND `password`=%s"
        cursor.execute(sql, (email, password, ))
        result = cursor.fetchone() 

        # 세션값 저장
        session['login'] = True
        session['fullname'] = result['fullname']
        session['email'] = result['email']

        return render_template('index.html')

@app.route('/auth/logout')
def logout():
    
    # 세션에서 제거
    session.pop('login', None)
    session.pop('fullname', None)
    session.pop('email', None)

    return redirect(url_for('login'))

@app.route('/auth/register', methods =['GET', 'POST']) 
def register():
    if request.method == 'POST':

        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        
        sql = "INSERT INTO `user` (`fullname`, `email`, `password`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (fullname, email, password, ))
        db.commit()
    
    return render_template('register.html')
    
# API Resource 라우팅을 등록
api.add_resource(Board, '/board')
api.add_resource(BoardArticle, '/board/<board_id>','/board/<board_id>/<board_article_id>')
api.add_resource(Dashboard, '/dashboard')

if __name__ == '__main__':
    app.run()