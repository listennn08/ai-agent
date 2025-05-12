import logging
from sqlalchemy.orm import Session

from app.models import DrinkPhoto

main_logger = logging.getLogger("sipp")


class DrinkPhotoRepository:
    def __init__(self, db: Session):
        main_logger.info("== Initialize DrinkPhotoRepository ==")
        self.db = db

    def get_drink_photo(self, sku: str) -> DrinkPhoto:
        return self.db.query(DrinkPhoto).filter(DrinkPhoto.sku == sku).first()
