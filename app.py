from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.raffleList
db2 = client.debateRoom

## HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')

## DebateRoom으로 이동하기
@app.route('/debateRoom')
def debateRoom():
    return render_template('debateRoom.html')

##라플 정보 가져오기
@app.route('/order', methods=['GET'])
def view_info():
    raffles = list(db.raffleList.find({}, {'_id': False}))
    return jsonify({'all_raffles': raffles})

##토론방 글쓰기
@app.route('/debateRoom2', methods=['POST'])
def write_debate():
    name_receive = request.form['name_give']
    password_receive = request.form['password_give']
    comment_receive = request.form['comment_give']

    doc = {'name': name_receive,
           'password': password_receive,
           'comment' : comment_receive,
    }

    db2.debate.insert_one(doc)

    return jsonify({'msg': '글쓰기가 완료되었습니다.'})

##토론방 글가져오기
@app.route('/debateRoom2', methods=['GET'])
def view_debates():
    debates = list(db2.debate.find({}, {'_id': False}))
    return jsonify({'all_debates': debates})

##토론방 글삭제하기
@app.route('/debateRoom/delete', methods=['POST'])
def delete_comment():
    name_receive = request.form['name_give']
    db2.debate.delete_one({'name': name_receive})

    return jsonify({'msg': '글이 삭제 되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)