from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.db.models import Base

engine = create_engine('sqlite:///finance.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
