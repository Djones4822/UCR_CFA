# App.py contains the main "driver" logic for the application

import os
from sqlalchemy import create_engine
from DiscoverPolicingScraper import DiscoverPolicingScraper


def get_db_url():
    """
    Returns the database connection URL
    The DB connection info can't be stored in the public repo (to keep out bad
    guys). Using environment variables is an easy way to keep the location
    and format uniform across platforms
    """
    return "postgresql://{0}:{1}@{2}/{3}".format(
        os.getenv("UCR_CFA_DB_USER"),
        os.getenv("UCR_CFA_DB_PASSWORD"),
        os.getenv("UCR_CFA_DB_HOST"),
        os.getenv("UCR_CFA_DB_NAME"))

engine = create_engine(get_db_url())


def get_db_info():
    """
    Returns a string providing information about the DB.
    Currently returns the Postgres version string
    """
    connection = engine.connect()
    result = connection.execute("select version() as v")

    version = str(result.first())

    if version is None:
        version = "Failed"

    return version


def scrape_all():
    """
    Kicks off scraping all sources
    """
    scrape_discover_policing()


def scrape_discover_policing():
    """
    Scrapes discoverpolicing.com
    """
    scraper = DiscoverPolicingScraper.createForDBOutput(engine)
    scraper.scrape()
