# AI was used to help create this connection between FastAPI, SQLAlchemy and MySQL

# got these imports from https://docs.sqlalchemy.org/en/21/orm/extensions/asyncio.html and AI
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo = True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


                                                                                                                            