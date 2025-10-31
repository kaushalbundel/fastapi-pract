from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()

# class for connecting sqlalchemy to the database
class Products(BASE):

    #giving name to the table
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index= True)
    description = Column(String)
    price = Column(String)
    quantity = Column(Float)