const testbtn=document.querySelector("#testbtn");
const qna=document.querySelector("#qna");

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
    var q=document.querySelector('.qBox');
    q.innerHTML=qnalist[qIdx].q;
    for(let i in qnalist[qIdx].a){
        addAnswer(qnalist[qIdx].a[i].answer, qIdx);
    }
}

function begin(){
    setTimeout(() => {
        testbtn.style.display="none";
        qna.style.display="block";
    }, 450);
    let qIdx=0;
    goNext(qIdx);
}