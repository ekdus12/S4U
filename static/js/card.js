//card가 안 뜬다 수정 ㄱ
function card(){
    fetch('tempData.json') //결과 json을 받을 예정
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('card-container');

        data.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <div class="album-wrapper">
            <div class="user-id">${item.userId}</div>
            <div class="album-cover" style="background-image: url('${item.cover}')"></div>
            </div>
            <div class="song-info">
            <strong>${item.title}</strong><br>
            <small>${item.desc}</small>
            </div>
        `; //이미지 임시
        container.appendChild(card);
        });
    });
}