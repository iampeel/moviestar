@app.route('/api/like', methods=['POST'])
def like_star():
    # like할 이름 받기
    name_receive = request.form['name_give']

    # 해당 이름에 관한 DB정보 빼오기
    target_star = db.mystar.find_one({'name': name_receive})

    current_like = target_star['like']

    new_like = current_like + 1

    db.mystar.update_one({'name': name_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '좋아요 완료'})