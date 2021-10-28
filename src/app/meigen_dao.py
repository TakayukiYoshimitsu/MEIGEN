from app.meigen_db import MeigenDto

from sqlalchemy.exc import SQLAlchemyError


class MeigenDao:
    """
    名言をDBから作成・取得・更新・削除するオブジェクト
    """
    def __init__(self, session):
        """
        DBとのsessionを初期化する
        """
        self.session = session

    def get_meigens_count(self):
        """
        DBに登録されている名言の個数を取得
        Returns:処理が正常：登録されている名言の個数
                処理が異常：False
        """
        meigen = self.session.query(MeigenDto).count()
        return meigen

    def get_meigen_by_id(self, meigen_id):
        """
        DBに登録されている1つの名言を取得
        Args:
            meigen_id:取得したい名言のID
        Returns:処理が正常：名言
                処理が異常：False
        """
        meigen = self.session.query(MeigenDto).filter_by(id=meigen_id).first()
        return meigen

    def insert_meigen(self, meigen_data):
        """
        名言をDBに追加する
        Args:
            meigen_data:入力された名言の内容
        Returns:処理が正常：True
                処理が異常：False
        """
        # DBに情報を追加するときのエラー処理
        try:
            self.session.add(meigen_data)
            self.session.commit()
            return True
        except SQLAlchemyError:
            self.session.rollback()
            return False

    def get_meigens(self):
        """
        DBから全ての名言情報を取得
        Returns:処理が正常：全ての名言情報
                処理が異常：False
        """
        # DBから情報を取得するときのエラー処理
        try:
            meigens = self.session.query(
                MeigenDto.id,
                MeigenDto.meigen,
                MeigenDto.author).all()
            return list(meigens)
        except SQLAlchemyError:
            return False

    def search_meigens(self, search_word):
        """
        DBから検索内容に一致した全ての名言情報を取得
        Args:
            search_word:入力された検索内容
        Returns:処理が正常：検索内容に一致した全ての名言情報
                処理が異常：False
        """
        try:
            # 名言で部分一致するレコードを返す
            search_meigens = self.session.query(
                MeigenDto.id,
                MeigenDto.meigen,
                MeigenDto.author).filter(MeigenDto.meigen.like(f'%{search_word}%')).all()
            if search_meigens:
                return list(search_meigens)

        # DBから情報を取得するときのエラー処理
        except SQLAlchemyError:
            return False

        try:
            # 作者で部分一致するレコードを返す
            search_meigens = self.session.query(
                MeigenDto.id,
                MeigenDto.meigen,
                MeigenDto.author).filter(MeigenDto.author.like(f'%{search_word}%')).all()
            if search_meigens:
                return list(search_meigens)

        # DBから情報を取得するときのエラー処理
        except SQLAlchemyError:
            return False
