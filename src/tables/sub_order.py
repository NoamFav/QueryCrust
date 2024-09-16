from sqlalchemy import Column, Integer,ForeignKey, Timestamp
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class SubOrder(Base):
    __tablename__ = 'sub_order'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('menu.id'))
    order_id = Column(Integer, ForeignKey('customer_orders.id'))

    order = relationship('CustomerOrders', back_populates='sub_orders')
    menu_item = relationship('Menu', back_populates='sub_orders')
