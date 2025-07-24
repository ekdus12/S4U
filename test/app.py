from flask import Flask, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

# Spotify 인증 및 객체 생성
cid = '2588cf31f44a407192315b32738a3605'
secret = '56c153ea371048919bbbbfafbead6e1d'
redirect_uri = 'http://127.0.0.1:3000/'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redirect_uri))

@app.route('/')
def index():
    # Spotify에서 아티스트 검색
    result = sp.search('iu', limit=2, type='artist')
    artists = result['artists']['items']
    # index.html에 artists 데이터 전달
    return render_template('index.html', artists=artists)

if __name__ == '__main__':
    app.run(port=3000)
