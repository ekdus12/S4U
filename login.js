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
            window.location.href = result.redirect_url;
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
            alert('로그아웃 되었습니다.');
            window.location.href = '/';
        } else {
            alert(result.message || '로그아웃에 실패했습니다.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('서버 오류가 발생했습니다.');
    });
}
