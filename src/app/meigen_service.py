from app.meigen_dao import MeigenDao
# from app.meigen_db import MeigenDto

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

        # 名言をランダムで取得
        # TODO サンプルで1を選択
        meigen_id = 1
        return self.database.get_meigen_by_id(meigen_id)