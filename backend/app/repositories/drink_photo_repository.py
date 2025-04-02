from sqlalchemy.orm import Session

from models import DrinkPhoto


class DrinkPhotoRepository:
    def __init__(self, db_session: Session):
        print("== Initialize DrinkPhotoRepository ==")
        self.db = next(db_session)

    def get_drink_photo(self, sku: str) -> DrinkPhoto:
        return self.db.query(DrinkPhoto).filter(DrinkPhoto.sku == sku).first()
