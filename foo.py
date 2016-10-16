from DiscoverPolicingScraper import DiscoverPolicingScraper
from sqlalchemy import create_engine
import os


def get_url():
    return "postgresql://{0}:{1}@{2}/{3}".format(
        os.getenv("UCR_CFA_DB_USER"),
        os.getenv("UCR_CFA_DB_PASSWORD"),
        os.getenv("UCR_CFA_DB_HOST"),
        os.getenv("UCR_CFA_DB_NAME"))

engine = create_engine(get_url())

x = DiscoverPolicingScraper.createForDBOutput(engine)

r = range(1,2)

x.scrape(r)
