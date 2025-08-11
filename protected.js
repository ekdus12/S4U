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
