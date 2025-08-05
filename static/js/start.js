const qna=document.querySelector("#qna");
const tpResult=document.querySelector("#tpResult");
const endpoint=8;

function goResult(){
    //결과 url 받아서 연결. 받아오는 대신 "/tempResult"을 사용해도 되긴 함
    window.location.href=tptargetUrl;
}

function addAnswer(answerText, qIdx){
    var a=document.querySelector('.aBox');
    var answer=document.createElement('button');
    answer.classList.add('answerlist');
    a.appendChild(answer);
    answer.innerHTML=answerText;
    answer.addEventListener("click", function(){
        var children=document.querySelectorAll('.answerlist');
        for(let i=0;i<children.length;i++){
            children[i].disabled=true;
            children[i].style.display='none';
        }
        goNext(++qIdx);
    }, false);
}

function goNext(qIdx){
    if(qIdx===endpoint){ //결과페이지로 이동하는 함수
        goResult();
    }
    var q=document.querySelector('.qBox');
    q.innerHTML=qnalist[qIdx].q;
    for(let i in qnalist[qIdx].a){
        addAnswer(qnalist[qIdx].a[i].answer, qIdx);
    }
}

function goBegin(){ //display 사용 안 하고, goNext함수 시작하게 하는 함수로 변경
    let qIdx=0;
    goNext(qIdx);
}