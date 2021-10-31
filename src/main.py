from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from starlette.templating import Jinja2Templates

import uvicorn

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.meigen_service import MeigenService
from app.meigen_db import MeigenRequest

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
def home_meigen(request: Request, db: Session = Depends(get_session)):
    """
    HOME画面画面に画面遷移、名言を表示
    Args:
        request: HOME画面取得リクエスト
        db: DBとの接続
    Returns:処理が正常：HOME画面のHTML,　ランダムで選ばれた名言の情報
    　　　　　処理が異常：500_エラー画面のHTML
    """
    # 表示する名言を取得
    meigen_service = MeigenService(db)
    meigen = meigen_service.get_meigen_by_random_id()

    # DBからデータを取得できなかった場合、500_エラー画面に遷移
    if not meigen:
        return templates.TemplateResponse("500_error.html", {"request": request})

    # HOME画面を表示
    return templates.TemplateResponse("home.html", {"request": request, "meigen": meigen})


@app.get("/entry", response_class=HTMLResponse)
def entry_meigen(request: Request):
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
            処理が異常：500_エラー画面のHTML
    """
    # 表示する名言を取得
    meigen_service = MeigenService(db)
    meigens = meigen_service.get_meigens()

    # DBからデータを取得できなかった場合、500_エラー画面に遷移
    if not meigens:
        return templates.TemplateResponse("500_error.html", {"request": request})

    # いちらん画面を表示
    return templates.TemplateResponse("meigen_list.html", {"request": request, "meigens": meigens})


@app.get("/confirm/{meigen_id}", response_class=HTMLResponse)
def confirm_meigen(request: Request, meigen_id: int, db: Session = Depends(get_session)):
    """
    かくにん画面画面に画面遷移、名言を表示
    Args:
        request: かくにん画面取得リクエスト
        meigen_id: かくにんする名言のID
        db: DBとの接続
    Returns:処理が正常：かくにん画面のHTML,　選ばれた名言の情報
    　　　　　処理が異常：500_エラー画面のHTML
    """
    # 表示する名言を取得
    meigen_service = MeigenService(db)
    meigen = meigen_service.get_meigen_by_id(meigen_id)

    # DBからデータを取得できなかった場合、500_エラー画面に遷移
    if not meigen:
        return templates.TemplateResponse("500_error.html", {"request": request})

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
    　　　　　処理が異常：いちらん画面に全ての名言情報を表示する形で遷移
    """
    meigen_service = MeigenService(db)
    meigens = meigen_service.search_meigens(search_word)

    # DBからデータを取得できなかった場合、一覧画面に再遷移
    if not meigens:
        meigens = meigen_service.get_meigens()
        # いちらん画面を表示
        return templates.TemplateResponse("meigen_list.html", {"request": request, "meigens": meigens})

    #   検索内容で絞り込み済みのいちらん画面を表示
    return templates.TemplateResponse("meigen_list.html", {"request": request, "meigens": meigens})


@app.get('/delete/{meigen_id}', status_code=201)
def delete_meigen(meigen_id: int, db: Session = Depends(get_session)):
    """
    名言を削除する
    Args:
        meigen_id: 削除するスケジュールのID
        db: DBとの接続

    Returns:処理が正常：True
            処理が正常：False
    """
    meigen_Service = MeigenService(db)
    success = meigen_Service.delete_meigen(meigen_id)

    # DBにスケジュールを削除できなかった場合、500_エラー画面に遷移
    if not success:
        return JSONResponse(status_code=500, content=item)


@app.exception_handler(StarletteHTTPException)
def custom_http_exception_handler(request, exc):
    """
    存在しないURLが叩かれた場合、/404にリダイレクト
    Returns:/404にリダイレクト
    """
    return RedirectResponse("/404")


@app.get('/404', response_class=HTMLResponse)
def not_found(request: Request):
    """
    404_エラー画面を表示
    Args:
        request: 404_エラー画面取得リクエスト
    Returns:404_エラー画面のHTML
    """
    return templates.TemplateResponse("404_error.html", {"request": request})


@app.get('/500', response_class=HTMLResponse)
def server_error(request: Request):
    """
    500: NotFound画面を表示
    :param request: InternalServerError画面取得リクエスト
    :return: 500_エラー画面のHTML
    """
    return templates.TemplateResponse("500_error.html", {"request": request})


@app.post('/entry', status_code=201)
def entry_meigen(meigen: MeigenRequest, db: Session = Depends(get_session)):
    """
    名言の登録
    Args:
        meigen: 入力された名言情報
        db: DBとの接続
    Returns:　500エラー
    """
    meigen_Service = MeigenService(db)
    success = meigen_Service.entry_meigen(meigen)

    # DBにスケジュールを登録できなかった場合、500_エラー画面に遷移
    if not success:
        return JSONResponse(status_code=500, content=item)


@app.post('/update/{meigen_id}', status_code=201)
def update_meigen(meigen: MeigenRequest, meigen_id: int, db: Session = Depends(get_session)):
    """
    名言の更新
    Args:
        meigen: 入力された名言の更新内容
        meigen_id:　更新する名言のID
        db:　DBとの接続
    Returns:　500エラー
    """
    meigen_Service = MeigenService(db)
    success = meigen_Service.update_meigen(meigen, meigen_id)

    # DBのスケジュールを更新できなかった場合、500_エラー画面に遷移
    if not success:
        return JSONResponse(status_code=500, content=item)


if __name__ == "__main__":
    uvicorn.run(app)