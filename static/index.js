function InsertWord() {
    const elements = document.getElementsByClassName('form')[0];
    let temp = document.createElement('div');
    let count = document.querySelectorAll('.word-input .content').length;
    temp.setAttribute('class', 'word-input');
    temp.innerHTML = `
        <span class="num">${count}</span>
        <div class="content">
            <textarea name="content" placeholder="단어를 입력해주세요." rows="2"></textarea>
        </div>
        <div class="mean">
            <textarea name="mean" placeholder="의미를 입력해주세요." rows="2"></textarea>
        </div>
    `;
    elements.appendChild(temp);
}

function DeleteWord() {
    const elements = document.getElementsByClassName('form')[0];
    elements.removeChild(elements.lastChild);
}

const delete_elements = document.getElementsByClassName("delete");
Array.from(delete_elements).forEach(function(element) {
    element.addEventListener('click', function() {
        if(confirm("정말로 삭제하시겠습니까?")) {
            location.href = this.dataset.uri;
        };
    });
});

var voices = [];

function setVoiceList() {
    voices = window.speechSynthesis.getVoices();
}
setVoiceList();
if (window.speechSynthesis.onvoiceschanged !== undefined) {
    window.speechSynthesis.onvoiceschanged = setVoiceList;
}

function speech(txt, lang) {
    if (!window.speechSynthesis) {
        alert("음성 재생을 지원하지 않는 브라우저입니다. Chrome, FireFox 등의 최신 브라우저를 이용하세요.");
        return;
    }
    var utterThis = new SpeechSynthesisUtterance(txt);
    utterThis.onend = function (event) {
        console.log('end');
    };
    utterThis.onerror = function (event) {
        console.log('error', event);
    };
    var voiceFound = false;
    for (var i = 0; i < voices.length; i++) {
        if (voices[i].lang.indexOf(lang) >= 0 || voices[i].lang.indexOf(lang.replace('-', '_')) >= 0) {
            utterThis.voice = voices[i];
            voiceFound = true;
        }
    }
    if (!voiceFound) {
        alert('voice not found');
        return;
    }
    utterThis.lang = lang;
    utterThis.pitch = 1;
    utterThis.rate = 0.8; //속도
    window.speechSynthesis.speak(utterThis);
}

function Select() {
    const path = window.location.pathname;
    const element = document.querySelectorAll('.list-option > div');
    if(path == '/sword/main/') element[0].setAttribute("class", "select");
    if(path == '/sword/mine/') element[1].setAttribute("class", "select");
    if(path == '/sword/like/') element[2].setAttribute("class", "select");
}

Select();

function HideList(type) {
    if(type == 'all') {
        var element1 = document.querySelector(`.word-all`);
        element1.removeAttribute('style');
        var element2 = document.querySelector(`.word-mark`);
        element2.setAttribute('style', 'display: none;');
    }
    else if(type == 'mark') {
        var element1 = document.querySelector(`.word-mark`);
        element1.removeAttribute('style');
        var element2 = document.querySelector(`.word-all`);
        element2.setAttribute('style', 'display: none;');
    }
}

function HideBookList(type) {
    if(type == 'all') {
        var elements = document.querySelectorAll('.list-option > div');
        elements[0].setAttribute('class', 'select');
        elements[1].removeAttribute('class');
        elements[2].removeAttribute('class');

        var element1 = document.querySelector(`.voca-book-all`);
        element1.removeAttribute('style');
        var element2 = document.querySelector(`.voca-book-mine`);
        element2.setAttribute('style', 'display: none;');
        var element3 = document.querySelector(`.voca-book-like`);
        element3.setAttribute('style', 'display: none;');
    }
    else if(type == 'mine') {
        var elements = document.querySelectorAll('.list-option > div');
        elements[0].removeAttribute('class');
        elements[1].setAttribute('class', 'select');
        elements[2].removeAttribute('class');

        var element1 = document.querySelector(`.voca-book-mine`);
        element1.removeAttribute('style');
        var element2 = document.querySelector(`.voca-book-all`);
        element2.setAttribute('style', 'display: none;');
        var element3 = document.querySelector(`.voca-book-like`);
        element3.setAttribute('style', 'display: none;');
    }
    else if(type == 'like') {
        var elements = document.querySelectorAll('.list-option > div');
        elements[0].removeAttribute('class');
        elements[1].removeAttribute('class');
        elements[2].setAttribute('class', 'select');

        var element1 = document.querySelector(`.voca-book-like`);
        element1.removeAttribute('style');
        var element2 = document.querySelector(`.voca-book-mine`);
        element2.setAttribute('style', 'display: none;');
        var element3 = document.querySelector(`.voca-book-all`);
        element3.setAttribute('style', 'display: none;');
    }
}

function Search(type) {
    const page_elements = document.getElementsByClassName(`page-link-${type}`);
    Array.from(page_elements).forEach(function(element) {
        element.addEventListener('click', function() {
            document.getElementById('type').value = type;
            document.getElementById('page').value = this.dataset.page;
            document.getElementById('searchForm').submit();
        });
    });

    const btn_search = document.getElementById(`btn_${type}_search`);
    btn_search.addEventListener('click', function() {
        document.getElementById('type').value = type;
        document.getElementById('kw').value = document.getElementById(`search_${type}_kw`).value;
        document.getElementById('page').value = 1;
        document.getElementById('searchForm').submit();
    });
}

Search('all');
Search('mine');
Search('like');