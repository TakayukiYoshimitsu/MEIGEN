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

function updateMeigen(meigen_id){
    // 登録する入力項目を取得する
    let Meigen = document.querySelector("#meigen").value;
    let Author = document.querySelector("#author").value;

    //　比較
    if (Meigen === ""){
      alert('名言が空欄です。')
    } else {
        if(window.confirm('更新してよろしいですか？')){

            // APIに送信するリクエストボディを作成
            let body = {
                meigen: Meigen,
                author: Author
            };

            // リクエストを送信
            fetch("/update/" + meigen_id, {
                // POSTメソッドで送信する
                method: "POST",
                // リクエストボディを設定
                body: JSON.stringify(body),
                // リクエストヘッダーを設定する
                headers: {
                    "Content-Type": "application/json"
                }
            }).then(response =>{
                if(response.ok){
                    alert('更新完了しました。')
                    // リクエスト送信後トップページに移行
                    window.location.href = "/"
                }else{
                    window.location.href = "/500"
                }
            })
        }
    }
}

function deleteMeigen(meigen_id){
   if(window.confirm('削除してよろしいですか？')){
   // 削除リクエスト発行を実装する
   fetch("/delete/" + meigen_id, {
        // GETメソッドで削除する
        method: "GET",
   }).then(response => {
        if (response.ok){
            alert('削除完了しました。')
            // リクエスト送信後トップページに移行する
            window.location.href = "/"
        }else{
            window.location.href = "/500"
        }
    })
   }
}