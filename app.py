import pymysql
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource

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

if __name__ == '__main__':
    app.run()