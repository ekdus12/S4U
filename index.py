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
@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/searchtab') #기존 search가 사라진 파일로 계속 경로를 설정해서 새파일 생성
def searchtab():
    #js에서 사용할 userId목록 전달
    user_ids=list(user.userId for user in User.query.all())
    print(user_ids) #서버 콘솔 확인용
    return render_template('searchtab.html', user_ids=user_ids)

@app.route('/playlist/<user_id>') #개인 유저별 플레이리스트를 보여주기 위함
def playlist(user_id):
    user = User.query.filter_by(userId=user_id).first()
    if not user: #유저 없으면 이동 안 함
        return redirect(url_for('searchtab'))
    return render_template('playlist.html', user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True, port=5500)
