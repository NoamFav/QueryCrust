from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association table for many-to-many relationship between Menu and Ingredient
class PizzaIngredient(Base):
    __tablename__ = 'pizza_ingredient'

    menu_id = Column(Integer, ForeignKey('menu.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'), primary_key=True)
    is_vegetarian = Column(Boolean)
    is_vegan = Column(Boolean)

    # Relationships
    menu = relationship("Menu", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="menus")
