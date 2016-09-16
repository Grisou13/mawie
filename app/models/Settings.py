# TODO: redo models with https://github.com/mardix/active-alchemy
from sqlalchemy import Column
from sqlalchemy import String

from app.models import db

class Settings(db.Model):
    __tablename__ = "settings"
    key = Column(String)
    value = Column(String)