const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

let minutes = 0;
let seconds = 0;

let minutes__input = $('.pomodoro__box-input-minutes');
let seconds__input = $('.pomodoro__box-input-seconds');

function refreshValue(){
    minutes = parseInt($('.pomodoro__box-input-minutes').value);
    seconds = parseInt($('.pomodoro__box-input-seconds').value);
}

function setItems(){
    localStorage.setItem('Mins', minutes);
    localStorage.setItem('Secs', seconds);
}

const checkTime = () => console.log(minutes, seconds);
// minutes__input.addEventListener('blur', () => {
// })

// seconds__input.addEventListener('blur', () => {
// })

function validateMinutes() {
    refreshValue();
    checkTime();
    if (minutes > 59){
        minutes__input.value = 59;
        refreshValue();
        setItems();
    }
    else if (minutes == "" || minutes == null || minutes < 0){
        minutes__input.value = 25;
        refreshValue();
        setItems();
    }
    else if (!Number.isInteger(minutes)){
        minutes__input.value = Math.floor(minutes);
        refreshValue();
        setItems();
    }
}

function validateSeconds(){
    refreshValue();
    checkTime();
    if (seconds > 59){
        seconds__input.value = 59;
        refreshValue();
        setItems();
    }
    else if (seconds == "" || seconds == null || seconds < 0){
        seconds__input.value = "00";
        refreshValue();
        setItems();
    }
    else if (!Number.isInteger(seconds)){
        seconds__input.value = Math.floor(seconds);
        refreshValue();
        setItems();
    }
}

//Test
let jack = $(".post");
jack.addEventListener('click', () => {
    alert('This post has been clicked.')
})