from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from starlette.templating import Jinja2Templates

import uvicorn

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.meigen_service import MeigenService

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
    名言を表示
    Args:
        request: HOME画面取得リクエスト
        db: DBとの接続

    Returns:HOME画面のHTML,処理が正常に行われない場合エラー番号500のHTML
    """
    # 表示する名言を取得
    meigen_service = MeigenService(db)
    meigen = meigen_service.get_schedule_by_id()

    # # DBからデータを取得できなかった時のエラー処理
    # if not schedules:
    #     print('sever error')
    #     # return templates.TemplateResponse("error500.html", {"request": request})

    # HOME画面を表示
    return templates.TemplateResponse("home.html", {"request": request, "meigen": meigen})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)