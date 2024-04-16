from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create engine and session
connection_url = 'postgresql://postgres:root@127.0.0.1:5432/Main_db'
engine = create_engine(connection_url)
Session = sessionmaker(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Add this line
session = Session()

