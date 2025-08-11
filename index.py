from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from models import db, User
import requests
#from werkzeug.security import generate_password_hash 비밀번호를 암호화할 때 사용

app = Flask(__name__)
app.secret_key = 'my_secret_key' # session 비밀키


# DB 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# 메인 페이지 (로그인 페이지)
@app.route('/', methods=['GET', 'POST'])
def goLogin():
    return render_template('login.html')
def kakao_login():
    data = request.json
    return jsonify({'status':'ok', 'nickname': data['nickname']})

# 로그인 파트
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    userId = data.get('user_id')
    nickname = data.get('nickname')

    # DB에서 사용자 검색
    user = User.query.filter_by(userId=userId, nickname=nickname).first()
    if user:
        session['user_id'] = userId
        return jsonify(success=True, message='로그인 성공!', redirect_url = url_for('protected'))
    else:
        return jsonify(success=False, message='아이디 또는 닉네임이 올바르지 않습니다.')
    
@app.route('/oauth/callback')
def oauth_callback():
    code = request.args.get('code')
    if not code:
        return redirect(url_for('goLogin'))
    
    #카카오에서 토큰 받기
    data = {
        'grant_type': 'authorization_code',
        'client_id': 'e53ec257a899fd2adc0aa192036f1967',  # REST API 키
        'redirect_uri': 'http://127.0.0.1:5500/oauth/callback',
        'code': code
    }
    resp = requests.post('https://kauth.kakao.com/oauth/token', data=data)
    token_json = resp.json()
    access_token = token_json.get('access_token')
    if not access_token:
        return redirect(url_for('goLogin'))
    
    # 사용자 정보 요청
    headers = {'Authorization': f'Bearer {access_token}'}
    user_resp = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)
    user_json = user_resp.json()
    kakao_id = user_json['id']
    kakao_nickname = user_json['kakao_account']['profile']['nickname']

    # DB에서 유저 검색 후 신규면 회원가입, 기존이면 로그인처럼 처리
    user = User.query.filter_by(userId=str(kakao_id)).first()
    if not user:
        user = User(userId=str(kakao_id), nickname=kakao_nickname)
        db.session.add(user)
        db.session.commit()
    session['user_id'] = user.userId

    # 이제 세션이 생성되었으니 protected로 이동
    return redirect(url_for('protected'))

    
# 로그인 후 페이지
@app.route('/protected')
def protected():
    if 'user_id' in session:
        return render_template('protected.html')
    else:
        return redirect(url_for('goLogin'))

# 로그아웃
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None) # session에서 로그인 정보 삭제
    return jsonify(success=True, message='로그아웃 성공!')


# 회원가입 페이지
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userId = request.form.get('userId')
        nickname = request.form.get('nickname')

        # 중복 체크
        if User.query.filter_by(userId=userId).first():
            return render_template('signup.html', error="이미 존재하는 ID 입니다.")
        
        # 회원가입 처리
        new_user = User(userId=userId, nickname=nickname)
        db.session.add(new_user)
        db.session.commit()

        # 수정요함 (구려서)
        return render_template('login.html')

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
