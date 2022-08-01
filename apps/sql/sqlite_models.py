import datetime
from apps.sql.sqlite_database import Base
from sqlalchemy import Column, VARCHAR, DATETIME


class Authorize(Base):
    __tablename__ = "authorize"

    uuid = Column(VARCHAR(512), primary_key=True, index=True)
    customer = Column(VARCHAR(512))
    create_time = Column(DATETIME, default=datetime.datetime.now())
    latest_update_time = Column(DATETIME)
    latest_expired_date = Column(DATETIME)
    expired_date = Column(DATETIME)
    
    




