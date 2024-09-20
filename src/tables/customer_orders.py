from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class CustomerOrders(Base):
    __tablename__ = 'customer_orders'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer_personal_information.id'))
    total_cost = Column(Float)
    delivery_eta = Column(DateTime)
    ordered_at = Column(DateTime)
    status = Column(String(10))
    password = Column(String(30))

#    customer = relationship('CustomerPersonalInformation', back_populates='orders')
#    sub_orders = relationship('SubOrder', back_populates='order')
#    delivery = relationship('Delivery', back_populates='order')
