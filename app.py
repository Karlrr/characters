from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient

# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.dbsparta

# 전역 변수
global name_selected

@app.route('/')
def home():
    return render_template('main.html')


@app.route('/input')
def information_input():
    return render_template('input.html')


@app.route('/intro')
def intro():
    return render_template('intro.html')

# API 역할을 하는 부분

# 1. 클라이언트가 준 정보 가져오기.
# 2. DB에 정보 삽입하기
# 3. 성공 여부 & 성공 메시지 반환하기


@app.route('/posting', methods=['POST'])
def posting_character():
    # 클라이언트가 준 이름 가져오기
    name_receive = request.form['name_give']
    # 클라이언트가 준 소속 가져오기
    group_receive = request.form['group_give']
    # 클라이언트가 준 사진url 가져오기
    portrait_receive = request.form['portrait_give']
    # 클라이언트가 준 간략 소개 가져오기
    short_desc_receive = request.form['short_desc_give']
    # 클라이언트가 준 상세 소개 가져오기
    long_desc_receive = request.form['long_desc_give']

    # DB에 삽입할 post 만들기
    doc = {
    'name': name_receive,
    'group': group_receive,
    'portrait': portrait_receive,
    'short_desc': short_desc_receive,
    'long_desc': long_desc_receive
    }

    # posting에 post 저장하기
    db.characterpost.insert_one(doc)
    # 성공 여부 & 성공 메시지 반환
    # ** 빈칸 있으면 알림 표시하는 기능 추가해야함

    return jsonify({'msg': '캐릭터 정보가 저장 되었습니다.'})


# 카드 생성
@app.route('/card', methods=['GET'])
def listing():
    cards = list(db.characterpost.find({}, {'_id': False}))
    return jsonify({'all_cards': cards})


# 캐릭터소개 페이지 연결
# 더럽게 안 됐는데 전역변수랑 elif 써서 성공
@app.route('/inform', methods=['POST', 'GET'])
def get_name():
    global name_selected
    if request.method == 'POST':
        name_selected = request.form['name_clicked']
        return jsonify({'msg':'이것은 name POST!'})
    elif request.method == 'GET':
            information = db.characterpost.find_one({'name': name_selected}, {'_id': False})
            return jsonify({'character_selected': information})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
