from app.meigen_dao import MeigenDao
from app.meigen_db import MeigenDto

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

    def get_meigen_by_random_id(self):
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

    def entry_meigen(self, meigen_data):
        """
        入力された内容をDBに登録できる形式に変換。
        Args:
            meigen_data:入力された名言の内容
        Returns:処理が正常：True
                処理が異常：False
        """
        meigen_record = MeigenDto(
            meigen=meigen_data.meigen,
            author=meigen_data.author,
        )
        return self.database.insert_meigen(meigen_record)

    def get_meigens(self):
        """
        登録されている名言情報の一覧を取得
        Returns:処理が正常：全ての名言情報
                処理が異常：False
        """
        return self.database.get_meigens()

    def get_meigen_by_id(self, meigen_id):
        """
        選択された名言を取得
        Returns:処理が正常:名言
                処理が異常:False
        """
        return self.database.get_meigen_by_id(meigen_id)

    def search_meigens(self, search_word):
        """
        検索内容に一致した全ての名言情報を取得
        Returns:処理が正常：検索に一致した全ての名言情報
                処理が異常：False
        """
        return self.database.search_meigens(search_word)

    def update_meigen(self, meigen_data, meigen_id):
        """
        DBに登録済みの名言情報を入力された内容で更新
        Args:
            meigen_data: 入力された名言の更新内容
            meigen_id: 更新する名言のID
        Returns:処理が正常：True
                処理が異常：False
        """
        return self.database.update_meigen(meigen_data, meigen_id)

    def delete_meigen(self, meigen_id):
        """
        選択された名言を削除する
        Args:
            meigen_id: 削除する名言のID

        Returns:処理が正常：True
                処理が異常：False
        """
        return self.database.delete_meigen(meigen_id)