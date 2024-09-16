from sqlalchemy import Column, Integer, String, Float, ForeignKey, Timestamp
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class CustomerOrders(Base):
    __tablename__ = 'customer_orders'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer_personal_information.id'))
    total_cost = Column(Float)
    delivery_eta = Column(Timestamp)
    ordered_at = Column(Timestamp)
    status = Column(String(10))
    password = Column(String(30))

    customer = relationship('CustomerPersonalInformation', back_populates='orders')
    sub_orders = relationship('SubOrder', back_populates='order')
    delivery = relationship('Delivery', back_populates='order')
