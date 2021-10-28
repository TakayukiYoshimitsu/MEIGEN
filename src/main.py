from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from starlette.templating import Jinja2Templates

import uvicorn

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.meigen_service import MeigenService
from app.meigen_db import MeigenRequest

import urllib.parse

import os

# Webアプリ用のオブジェクトを初期化
app = FastAPI()

# 静的ファイル(css, js)をマウント
app.mount("/static", StaticFiles(directory="static"), name="static")

# ページのテンプレートを読み込む
templates = Jinja2Templates(directory="templates/")

# DBとの接続
engine = create_engine("sqlite:///meigen.db", connect_args={"check_same_thread": False})
db_session = sessionmaker(bind=engine)


def get_session():
    """
    DBとのセッションを取得
    Returns:
    """
    session = db_session()
    try:
        yield session
    except:
        session.close()


@app.get("/", response_class=HTMLResponse)
def meigen_home(request: Request, db: Session = Depends(get_session)):
    """
    HOME画面画面に画面遷移、名言を表示
    Args:
        request: HOME画面取得リクエスト
        db: DBとの接続

    Returns:処理が正常：HOME画面のHTML,　ランダムで選ばれた名言の情報
    　　　　　処理が異常：エラー番号500のHTML
    """
    # 表示する名言を取得
    meigen_service = MeigenService(db)
    meigen = meigen_service.get_meigen_by_random_id()

    # # DBからデータを取得できなかった時のエラー処理
    # if not meigen:
    #     print('sever error')
    #     return templates.TemplateResponse("error500.html", {"request": request})

    # HOME画面を表示
    return templates.TemplateResponse("home.html", {"request": request, "meigen": meigen})


@app.get("/entry", response_class=HTMLResponse)
def meigen_entry(request: Request):
    """
    とうろく画面に遷移
    Args:
        request: とうろく画面取得リクエスト
    """
    # とうろく画面を表示
    return templates.TemplateResponse("entry.html", {"request": request})


@app.get("/meigen_list", response_class=HTMLResponse)
def meigen_list(request: Request, db: Session = Depends(get_session)):
    """
    いちらん画面に遷移
    Args:
        request: いちらん画面取得リクエスト
        db: DBとの接続

    Returns:処理が正常：いちらん画面のHTML,　全ての名言情報
            処理が異常：エラー番号500のHTML
    """
    # 表示する名言を取得
    meigen_service = MeigenService(db)
    meigens = meigen_service.get_meigens()

    # # DBからデータを取得できなかった時のエラー処理
    # if not meigen:
    #     print('sever error')
    #     return templates.TemplateResponse("error500.html", {"request": request})

    # いちらん画面を表示
    return templates.TemplateResponse("meigen_list.html", {"request": request, "meigens": meigens})


@app.get("/confirm/{meigen_id}", response_class=HTMLResponse)
def meigen_confirm(request: Request, meigen_id: int, db: Session = Depends(get_session)):
    """
    かくにん画面画面に画面遷移、名言を表示
    Args:
        request: かくにん画面取得リクエスト
        meigen_id: かくにんする名言のID
        db: DBとの接続

    Returns:処理が正常：かくにん画面のHTML,　選ばれた名言の情報
    　　　　　処理が異常：エラー番号500のHTML
    """
    # 表示する名言を取得
    meigen_service = MeigenService(db)
    meigen = meigen_service.get_meigen_by_id(meigen_id)

    # # DBからデータを取得できなかった時のエラー処理
    # if not meigen:
    #     print('sever error')
    #     return templates.TemplateResponse("error500.html", {"request": request})

    # かくにん画面を表示
    return templates.TemplateResponse("confirm.html", {"request": request, "meigen": meigen})


@app.get('/search/{search_word}', response_class=HTMLResponse)
def search_meigen(request: Request, search_word: str, db: Session = Depends(get_session)):
    """
    いちらん画面画面に画面遷移、検索内容に一致した名言を表示
    Args:
        request: いちらん画面取得リクエスト
        search_word: 入力された検索ワード
        db: DBとの接続

    Returns:処理が正常：いちらん画面のHTML,　検索内容に一致した名言の情報
    　　　　　処理が異常：エラー番号500のHTML
    """
    meigen_service = MeigenService(db)
    meigens = meigen_service.search_meigens(search_word)

    # # DBからデータを取得できなかった時のエラー処理
    # if not meigens:
    #     print('sever error')
    #     return templates.TemplateResponse("error500.html", {"request": request})

    return templates.TemplateResponse("meigen_list.html", {"request": request, "meigens": meigens})


@app.post('/entry', status_code=201)
def entry_meigen(meigen: MeigenRequest, db: Session = Depends(get_session)):
    """
    スケジュールの登録
    :param meigen: 登録するスケジュール
    :param db: DBとの接続

    """
    meigen_Service = MeigenService(db)
    meigen_Service.entry_meigen(meigen)
    # TODO
    # success = meigen_Service.entry_meigen(meigen)
    # DBにスケジュールを登録できなかった時のエラー処理    :return: 処理が正常に行われない場合はエラー番号500
    # if not success:
    #     return JSONResponse(status_code=status.HTTP_500_CREATED, content=item)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)