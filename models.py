from database import Base
from sqlalchemy import Column,Integer,String

class Students(Base):
    __tablename__="students"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,unique=True)
    dept=Column(String,nullable=False)
    fees=Column(Integer)
    
