from AgencyDBWriter import AgencyDBWriter
from AgencyScreenWriter import AgencyScreenWriter


class AgencyScraper(object):
    SLEEP_TIME = 5

    def __init__(self, writer=None):
        if writer is None:
            writer = AgencyScreenWriter
        self.writer = writer

    @classmethod
    def createForDBOutput(cls, sa_engine):
        return cls(AgencyDBWriter(sa_engine))

    @classmethod
    def createForScreenOutput(cls):
        return cls(AgencyScreenWriter)
