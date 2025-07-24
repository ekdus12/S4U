// 로그인 - 로그아웃의 구체적인 내용은 수정 필요

function login() {
    const userId = document.getElementById('inputID').value;
    const userNickname = document.getElementById('inputNickname').value;

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, nickname: userNickname })
    })
    .then(res => res.json())
    .then(result => {
        if (result.success) {
            document.getElementById('userInfo').style.display = 'none';
            document.getElementById('start').style.display = 'block';
            document.getElementById('kakaoLogin').style.display='none';
        } else {
            alert(result.message || '로그인 실패');
        }
    })
    .catch(err => {
        console.error(err);
        alert('서버 오류');
    });
}


function logout() {
    fetch('/logout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            document.getElementById('userInfo').classList.remove('hidden');
            document.getElementById('start').classList.add('hidden');
        } else {
            alert(result.message || '로그아웃에 실패했습니다.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('서버 오류가 발생했습니다.');
    });
}
