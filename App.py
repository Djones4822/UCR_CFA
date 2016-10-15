import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def get_url():
    return "postgresql://{0}:{1}@{2}/{3}".format(
        os.getenv("UCR_CFA_DB_USER"),
        os.getenv("UCR_CFA_DB_PASSWORD"),
        os.getenv("UCR_CFA_DB_HOST"),
        os.getenv("UCR_CFA_DB_NAME"))

engine = create_engine(get_url())
Session = sessionmaker(bind=engine)


def get_db_info():
    connection = engine.connect()
    result = connection.execute("select version() as v")

    version = str(result.first())

    if version is None:
        version = "Failed"

    return version


def scrape():
    return "Not implemented"
