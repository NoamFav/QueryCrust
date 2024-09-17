from sqlalchemy import Column, Integer,Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Discounts(Base):
    __tablename__ = 'discounts'

    id = Column(Integer, primary_key=True)
    used = Column(Boolean)