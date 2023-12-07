# Description: This file contains the database configuration and session management code.
from dotenv import load_dotenv
import os
from  sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
URL_DATABASE = f'mysql+pymysql://root:{DB_PASSWORD}@localhost:3306/{DB_NAME}'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

