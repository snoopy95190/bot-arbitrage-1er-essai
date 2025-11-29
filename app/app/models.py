from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class ProductScan(Base):
    __tablename__ = 'product_scan'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    source_price = Column(Numeric)
    amazon_price = Column(Numeric, nullable=True)
    marge = Column(Numeric, nullable=True)
    validated = Column(Boolean, default=False)
    scanned_at = Column(DateTime, default=datetime.datetime.utcnow)

def get_session(db_url='sqlite:///bot_arbitrage.db'):
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
