from sqlalchemy import create_engine, Column, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

# 　ベースモデルを作成
Base = declarative_base()
# DBと接続するオブジェクト
engine = create_engine("sqlite:///meigen.db", echo=True)


class MeigenRequest(BaseModel):
    """
    アプリに送信されるmeigenテーブルのリクエスト形式を定義する
    """
    meigen: str
    author: str


class MeigenDto(Base):
    """
    DBのScheduleテーブルとやり取りするデータ形式を定義する
    """
    # SQLでのテーブル名を定義
    __tablename__ = "meigen"

    # scheduleテーブルのカラムを定義
    id = Column(Integer, primary_key=True)
    meigen = Column(String(255))
    author = Column(String(255))

    def convert_dict(self):
        """
        辞書形式に変換する
        :return:
        """
        return {
            "id": self.id,
            "meigen": self.meigen,
            "author": self.author,
        }


Base.metadata.create_all(engine)