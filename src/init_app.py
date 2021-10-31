from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.meigen_dao import MeigenDao
from src.app.meigen_db import MeigenDto


def init_app():
    engine = create_engine("sqlite:///meigen.db")
    session = sessionmaker(bind=engine)()
    meigen_database = MeigenDao(session)
    init_meigen_data = [
        MeigenDto(meigen="なんでもやってみなはれ、やらなわからしまへんで",
                  author="鳥井信治郎"),
        MeigenDto(meigen="人はそれぞれ事情をかかえ、平然と生きている",
                  author="伊集院静"),
        MeigenDto(meigen="「負けたことがある」というのが　いつか　大きな財産になる",
                  author="マンガ「SLAM　DUNK」"),
    ]

    for data in init_meigen_data:
        meigen_database.insert_meigen(data)


if __name__ == "__main__":
    init_app()
