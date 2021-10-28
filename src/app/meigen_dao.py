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
        Returns:処理が正常：名言
                処理が異常：False
        """
        meigen = self.session.query(MeigenDto).filter_by(id=meigen_id).first()
        return meigen

    def insert_meigen(self, meigen_data):
        """
        名言をDBに追加する
        :param meigen_data:  名言オブジェクト
        :return: 処理が正常：True
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
