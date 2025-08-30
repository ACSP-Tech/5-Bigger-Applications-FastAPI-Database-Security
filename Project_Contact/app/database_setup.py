#defining database connection

from sqlmodel import create_engine #database connection takes in db url

database_url = "sqlite:///kodecamp.db" #for sql lite

#turn on support for configuration
config = {"check_same_thread": False}

connection = create_engine(database_url, connect_args=config)