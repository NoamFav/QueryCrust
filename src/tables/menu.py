from sqlalchemy import Column, Integer, String, Float, event
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import select, func

Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    price = Column(Float)
    category = Column(String(10))


@event.listens_for(Menu, 'before_insert')
def set_menu_id(connection, target):
    # Define category codes
    category_codes = {'pizza': 1, 'drink': 2, 'dessert': 3}
    category_code = category_codes.get(target.category.lower())

    if category_code is None:
        raise ValueError('Invalid category')

    # Calculate the ID range based on category
    start_id = category_code * 1000
    end_id = start_id + 999

    # Use SQLAlchemy's select() to query for the max id in the range
    stmt = select(func.max(Menu.id)).where(Menu.id.between(start_id, end_id))

    # Execute the select statement using the connection
    result = connection.execute(stmt)
    max_id = result.scalar()

    # Assign the new ID
    target.id = (max_id + 1) if max_id else (start_id + 1)
