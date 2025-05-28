from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
import sqlite3

# Create the engine with SQLite settings
engine = create_engine(
    'sqlite:///finance.db',
    echo=False,
    connect_args={'check_same_thread': False}
)

# Enable foreign key support for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Session factory
Session = sessionmaker(bind=engine)
