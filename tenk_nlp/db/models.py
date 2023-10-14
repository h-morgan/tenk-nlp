from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

import os

Base = declarative_base()


class Company(Base):
    __tablename__: str = "company"

    id = Column(String(36), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    ticker = Column(String(10))
    cik = Column(Integer, nullable=False)
    cusip = Column(Integer)
    exchange = Column(String)
    is_delisted = Column(Boolean)
    category = Column(String)
    sector = Column(String)
    industry = Column(String)
    sic = Column(Integer)
    sic_sector = Column(String)
    sic_industry = Column(String)
    fama_sector = Column(String)
    fama_industry = Column(String)
    currency = Column(String)
    location = Column(String)
    created_on = Column(DateTime(), nullable=False)
