from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    # MySQL requires a length for String columns used in indexes or tables
    hcp_name = Column(String(255), index=True) 
    interaction_type = Column(String(100))
    sentiment = Column(String(50))
    topics_discussed = Column(String(1000))
    date = Column(DateTime, default=datetime.datetime.utcnow)