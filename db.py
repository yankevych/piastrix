from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StdPay(Base):
    __tablename__ = 'std_pay3'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False, default='')
    description = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=False), default=None)
    shop_order_id = Column(Integer, unique=True, default=None)
    pay_sys_id = Column(Integer, unique=True, default=None)
    shop_refund = Column(Float, default=None)


