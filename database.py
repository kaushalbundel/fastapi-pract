
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# to create a database a session should be created. That session is called whenever we need to access the data

# the syntax for this db url is "postgresql://username:password@localhost:portnumber/dbName"
# username is always postgres and port for local machine is always 5432. dbName is the database name that can vary
db_url = "postgresql://postgres:0205kb@localhost:5432/fastapi"

# engine is the way a db is connected to a session
engine = create_engine(db_url)

# autoflush, default is True, This ensures that the session is consistent. If I inserted an item and I want to access the inserted item in the same session. Autoflush enables me to do that
# autocommit, default is False. Every data base employs all or nothing. It means all the instructions that have been given together should all execute together. If these are not executed in tandom then that may create issues in the overall database structure.
SessionLocal = sessionmaker( autoflush=False, autocommit = False, bind = engine)