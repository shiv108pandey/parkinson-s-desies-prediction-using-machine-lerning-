from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class UserInput(Base):
    __tablename__ = "userinputs"
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    patient_name = Column(String)
    age = Column(Integer)
    location = Column(String)
    
    def __repr__(self):
        return f"{self.patient_name} ({self.age})"

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True)
    pid = Column(Integer, ForeignKey('userinputs.id'))
    spiral_img_path = Column(String)
    wave_img_path = Column(String)
    predict_date = Column(DateTime, default=datetime.utcnow)

# Database initialization
if __name__ == "__main__":
    engine = create_engine('sqlite:///project_db.sqlite3')
    Base.metadata.create_all(engine)
