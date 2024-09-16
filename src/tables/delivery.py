from sqlalchemy import Column, Integer, ForeignKey, Timestamp
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Delivery(Base):
    __tablename__ = 'delivery'

    delivered_by = Column(Integer, ForeignKey('delivery_driver.id'))
    order_id = Column(Integer, ForeignKey('customer_orders.id'), primary_key=True)

    driver = relationship('DeliveryDriver', back_populates='deliveries')
    order = relationship('CustomerOrders', back_populates='delivery')