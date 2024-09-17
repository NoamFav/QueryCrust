from sqlalchemy import Column, Integer, String, Float, event
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    price = Column(Float)
    category = Column(String(10))

    sub_orders = relationship('SubOrder', back_populates='menu_item')


@event.listens_for(Menu, 'before_insert')
def set_menu_id(mapper, connection, target):
    # Define category codes
    category_codes = {'pizza': 1, 'drink': 2, 'dessert': 3}
    category_code = category_codes.get(target.category.lower())
    if category_code is None:
        raise ValueError('Invalid category')

    # Calculate the ID range based on category
    start_id = category_code * 1000
    end_id = start_id + 999

    # Retrieve the current maximum ID in the category range
    result = connection.execute(
        f"SELECT MAX(id) FROM menu WHERE id BETWEEN {start_id} AND {end_id}"
    )
    max_id = result.scalar()

    # Assign the new ID
    target.id = (max_id + 1) if max_id else (start_id + 1)
