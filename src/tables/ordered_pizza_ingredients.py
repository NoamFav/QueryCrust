from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association table for many-to-many relationship between Menu and Ingredient
class OrderedIngredient(Base):
    __tablename__ = 'ordered_pizza_ingredients'

    order_id = Column(Integer, ForeignKey('customer_orders.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'), primary_key=True)


    # Relationships
    customer_orders = relationship("CustomerOrder", back_populates="ingredients")
    ingredient = relationship("Ingredient")


