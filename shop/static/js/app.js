var showTime = function() {
    var disp = document.getElementById('clock');
    var meridian = "AM"
    var myDate = new Date();
    var hour = myDate.getHours();
    var minute = myDate.getMinutes();
    var second = myDate.getSeconds();

    if (hour > 11) {
        meridian = "PM"
    }

    if (hour >= 12) {
        hour = hour - 12
    };

    if (minute < 10) {
        minute = "0" + minute
    };

    if (second < 10) {
        second = "0" + second
    };

    currentTime = hour + ":" + minute + ":" + second + meridian;
    disp.innerHTML = currentTime;

};
showTime();
setInterval(showTime, 1000);