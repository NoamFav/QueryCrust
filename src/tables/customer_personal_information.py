from sqlalchemy import Column, Integer, String, DateTime, select, func, event
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

from base import Base


class CustomerPersonalInformation(Base):
    __tablename__ = 'customer_personal_information'

    id = Column(Integer, primary_key=True)
    address = Column(Integer)
    birthday = Column(DateTime)
    phone_number = Column(Integer)
    gender = Column(String(18))
    previous_orders = Column(Integer)
    age = Column(Integer)

    orders = relationship('CustomerOrders')


@event.listens_for(CustomerPersonalInformation, 'before_insert')
def auto_increment_menu_id(connection, target):
    # Use SQLAlchemy's select() to query for the max id in the Menu table
    stmt = select(func.max(CustomerPersonalInformation.id))

    # Execute the select statement using the connection
    result = connection.execute(stmt)
    max_id = result.scalar()

    # Assign the new ID by incrementing the max id
    target.id = (max_id + 1) if max_id else 1
