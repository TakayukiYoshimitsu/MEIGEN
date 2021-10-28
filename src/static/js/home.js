function home(){
    window.location.href = "/"
}

function home1(){
    window.location.href = "/entry"
}

function home2(){
    window.location.href = "/meigen_list"
}

var now = new Date();
function LoadDate(){
    // 現在日付を表示
    var target = document.getElementById("Date");
    var Year = now.getFullYear();
    var Month = now.getMonth()+1;
    var Date = now.getDate();

    // 桁数が一桁の場合、0を先頭に足す
    target.innerHTML = Year + "年" + ('0' + Month).slice(-2) + "月" + ('0' + Date).slice(-2) + "日";
}

function LoadTime(){
    // 現在時刻を表示
    var now = new Date();
    var target = document.getElementById("Time");
    var Hour = now.getHours();
    var Min = now.getMinutes();
    var Sec = now.getSeconds();

    // 桁数が一桁の場合、0を先頭に足す
    target.innerHTML = ('0' + Hour).slice(-2) + ":" + ('0' + Min).slice(-2) + ":" + ('0' + Sec).slice(-2);
}
// 毎秒ごとに時刻表示を更新
setInterval('LoadTime()',1000);

// 30分ごとに表示する名言を更新
setInterval('home()',1800000);

