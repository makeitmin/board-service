import pymysql
from flask import Flask, jsonify
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
        cursor.execute(sql, (args["id"], ))
        db.commit()
        
        return jsonify(status = "success", result = {"id": args["id"]})

    # API Resource 라우팅을 등록
    api.add_resource(Board, '/board')

if __name__ == '__main__':
    app.run()