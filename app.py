from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def show_stars():
    movie_star = list(db.mystar.find({}, {'_id': False}).sort('like', -1))
    return jsonify({'movie_stars': movie_star})


@app.route('/api/like', methods=['POST'])
def like_star():
    # like할 이름 받기
    name_receive = request.form['name_give']

    # 해당 이름에 관한 DB정보 빼오기
    target_star = db.mystar.find_one({'name': name_receive})
    # 해당 사람의 like정보 입수
    current_like = target_star['like']
    # like 수 +1
    new_like = current_like + 1
    # DB 수정
    db.mystar.update_one({'name': name_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '좋아요 완료'})


@app.route('/api/delete', methods=['POST'])
def delete_star():
    # 이름을 받아옴
    name_receive = request.form['name_give']
    # DB에서 삭제
    db.mystar.delete_one({'name': name_receive})

    return jsonify({'msg': '삭제 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
