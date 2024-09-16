from sqlalchemy import Column, Integer, String, Timestamp
from sqlalchemy.orm import relationship, declarative_base
Base = declarative_base()

class DeliveryDriver(Base):
    __tablename__ = 'delivery_driver'

    id = Column(Integer, primary_key=True)
    delivery_area = Column(String(8))
    last_delivery = Column(Timestamp)

    deliveries = relationship('Delivery', back_populates='driver')
