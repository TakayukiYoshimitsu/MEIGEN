function home(){
    // HOME画面に画面遷移
    window.location.href = "/"
}

function entry(){
    // とうろく画面に画面遷移
    window.location.href = "/entry"
}

function meigenList(){
    // いちらん画面に画面遷移
    window.location.href = "/meigen_list"
}

function confirm(id){
    // かくにん画面に画面遷移
    window.location.href = "/confirm/" + id
}

function searchMeigen() {
    // 検索リクエスト発行
    let searchWord = document.querySelector("#search-word").value;

    if (searchWord == ""){
        window.location.href = "/meigen_list"
    }else{
        window.location.href = "/search/" + searchWord
    }
}