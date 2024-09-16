from sqlalchemy import Column, Integer, String, Timestamp
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class CustomerPersonalInformation(Base):
    __tablename__ = 'customer_personal_information'

    id = Column(Integer, primary_key=True)
    address = Column(Integer)
    birthday = Column(Timestamp)
    phone_number = Column(Integer)
    gender = Column(String(18))
    previous_orders = Column(Integer)
    age = Column(Integer)

    orders = relationship('CustomerOrders', back_populates='customer')
