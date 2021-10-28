from app.meigen_dao import MeigenDao
# from app.meigen_db import MeigenDto

import random

class MeigenService:
    """
    名言表示システムのロジックを記載するオブジェクト
    """

    def __init__(self, session):
        """
        インスタンスを初期化
        """
        self.database = MeigenDao(session)

    def get_schedule_by_id(self):
        """
        DBに登録されている1つの名言をランダムで取得
        Returns:処理が正常:名言
                処理が異常:False
        """
        # DBに登録されている名言の個数をカウント
        meigens_count = self.database.get_meigens_count()

        # 名言をランダムで取得
        meigen_id = random.randint(1, meigens_count)
        return self.database.get_meigen_by_id(meigen_id)