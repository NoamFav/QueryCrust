from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

from src.functions.customer_order_utility import OrderContainer
from src.tables.database import *
import mysql.connector

engine = create_engine('sqlite:///memory')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
print(Base.metadata.tables.keys())

print("Adding mock data...")
pizza_item = Menu(name='Margherita', price=10.0, category='pizza')

