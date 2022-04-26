let countdown;

const minutes = $('.pomodoro__minutes')
const seconds = $('.pomodoro__seconds')
const cookie = getCookie('csrftoken');


// async function getData(url){
//     const response = await fetch(url);
//     const data = await response.json();
//     return data
// }

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getTask(){
    const task = $('input[type="radio"]:checked').id;
    return task
}

function pomodoro(){
    console.log('muffin')
    return {

        firstSession: true,
        completed: false,
        started: false,
        totalSeconds: 0,

        defTime: {
            minutes: 0,
            seconds: 0,
        },

        time: {
            minutes: 0,
            seconds: 0,
            totalTime: 0,
        },

        async getData(){
            const response = await(fetch('pomodoro/time/'))
            if (response.ok){
                const data = await response.json()
                this.time.minutes = data.minutes
                this.time.seconds = data.seconds
            } else {
                console.log('Could not get the data')
            }
        },

        init(){
            this.getData().then(() => {
                this.started = false;
                this.firstSession = true;
                this.time.totalTime = (parseInt(this.time.minutes) * 60) + parseInt(this.time.seconds);

                this.defTime.minutes = parseInt(this.time.minutes);
                this.defTime.seconds = parseInt(this.time.seconds);

                this.time.minutes = this.defTime.minutes < 10 ? "0" + this.defTime.minutes : this.defTime.minutes;
                this.time.seconds = this.defTime.seconds < 10 ? "0" + this.defTime.seconds : this.defTime.seconds;
            })
        },

        startPomodoro(){

            this.started = true;
        
            this.totalSeconds = this.time.totalTime

            clearInterval(countdown);

            this.firstSession = false;

            countdown = setInterval(() => {
                console.log(this.time.totalTime);
                this.time.totalTime--;
                let minutesRem = Math.floor(this.time.totalTime/ 60);
                let secondsRem = this.time.totalTime % 60;

                this.updateTime(minutesRem, secondsRem);
                this.checkCompleted();

            }, 1000)
        },

        stopPomodoro(){
            clearInterval(countdown);
            this.started = false;
            this.time.minutes = this.defTime.minutes < 10 ? "0" + this.defTime.minutes : this.defTime.minutes;
            this.time.seconds = this.defTime.seconds < 10 ? "0" + this.defTime.seconds : this.defTime.seconds;
            this.time.totalTime = this.defTime.minutes * 60 + this.defTime.seconds;
            this.firstSession = true;
            this.init()
        },

        pausePomodoro(){
            clearInterval(countdown);
            this.started = false;
        },

        updateTime(remMins, remSeconds){
            this.time.minutes = remMins < 10 ? "0" + remMins : remMins;
            this.time.seconds = remSeconds < 10 ? "0" + remSeconds : remSeconds;
        },

        checkCompleted(){
            if (this.time.minutes == "00" && this.time.seconds == "00"){
                alert('Over');
                const data = {
                    task: getTask(),
                    time: this.totalSeconds
                }
                const url = 'pomodoro/completed/'

                const response = this.sendAjaxRequest(url, data).then((data) => {
                    this.stopPomodoro()
                    if (data.ok){
                        data.json().then(message => console.log(message.Message))
                        window.location = '/'
                    }
                    
                })
                // alert(`Completed ${taskSelected} for a time of ${duration} seconds`);
            }
        },

        async sendAjaxRequest(url, data){
            const response = fetch(url, {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': cookie,
                }
            })
            return response
        }

    }
}

