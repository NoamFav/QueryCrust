from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Ingredient(Base):
    __tablename__ = 'ingredient'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    price = Column(Float)
    is_vegetarian = Column(Boolean)
    is_vegan = Column(Boolean)

    menus = relationship("PizzaIngredient", back_populates="ingredient")
