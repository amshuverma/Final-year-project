let countdown;

let taskSelected = null;
let duration = null;

const radioBtns = $$('.task__radio-btn');
const timeInputs = $$('.pomodoro__box-input');

function alertStarted(){
    taskSelected = $('input[name="task"]:checked').id;
    duration = parseInt($('.pomodoro__box-input-seconds').value) + parseInt($('.pomodoro__box-input-minutes').value * 60);
    alert(`Started ${taskSelected} for a time of ${duration} seconds.`)
}

function disableRadioAndInput(){
    radioBtns.forEach(btn => btn.disabled = true);
    timeInputs.forEach(input => input.disabled = true);  
}

function enableRadioAndInput(){
    radioBtns.forEach(btn => btn.disabled = false);
    timeInputs.forEach(input => input.disabled = false);  
}

function pomodoro(){
    console.log('muffin');

    return {
        firstSession: true,
        completed: false,
        started: false,
        defTime: {
            minutes: 00,
            seconds: 10,
        },

        time: {
            minutes: 0,
            seconds: 0,
            totalTime: 0,
        },

        init(){
            this.started = false;

            this.time.totalTime = (parseInt(localStorage.getItem('Mins')) * 60) + parseInt(localStorage.getItem('Secs'));

            this.defTime.minutes = parseInt(localStorage.getItem('Mins'));
            this.defTime.seconds = parseInt(localStorage.getItem('Secs'));

            this.time.minutes = this.defTime.minutes < 10 ? "0" + this.defTime.minutes : this.defTime.minutes;
            this.time.seconds = this.defTime.seconds < 10 ? "0" + this.defTime.seconds : this.defTime.seconds;
        },

        startPomodoro(){
            this.started = true;
            clearInterval(countdown);
            if (this.firstSession == true){
                alertStarted();
            }
            disableRadioAndInput();
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
            enableRadioAndInput();
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
                this.stopPomodoro();
                alert(`Completed ${taskSelected} for a time of ${duration} seconds`);
            }
        }

    }
}

