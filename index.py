from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# 메인 페이지 (로그인 페이지)
@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
def kakao_login():
    data = request.json
    return jsonify({'status':'ok', 'nickname': data['nickname']})

# 로그인 파트(수정 필요)
@app.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    userId = data.get('user_id')
    nickname = data.get('nickname')

    # 실제 DB에서 검색
    user = User.query.filter_by(userId=userId, nickname=nickname).first()
    if user:
        # TODO: 로그인 상태 유지(세션/JWT 등)
        return jsonify(success=True, message='로그인 성공!')
    else:
        return jsonify(success=False, message='아이디 또는 닉네임이 올바르지 않습니다.')

# 로그아웃 (실제로는 세션/토큰 삭제 필요)
@app.route('/logout', methods=['POST'])
def api_logout():
    return jsonify(success=True, message='로그아웃 성공!')


# 회원가입 페이지
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userId = request.form.get('userId')
        nickname = request.form.get('nickname')

        # 중복 체크
        if User.query.filter_by(userId=userId).first() or User.query.filter_by(nickname=nickname).first():
            return render_template('signup.html', error="이미 존재하는 ID 또는 닉네임입니다.")
        
        # 회원가입 처리
        user = User(userId=userId, nickname=nickname)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))  # 로그인 페이지로 이동
    return render_template('signup.html')

# 기타 페이지
@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/survey')
def survey():
    return render_template('survey.html')

if __name__ == '__main__':
    app.run(debug=True, port=5500)
