from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from base import Base

class DeliveryDriver(Base):
    __tablename__ = 'delivery_driver'

    id = Column(Integer, primary_key=True)
    delivery_area = Column(String(8))
    last_delivery = Column(DateTime)

    deliveries = relationship('Delivery', back_populates='driver')
