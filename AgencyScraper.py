from AgencyDBWriter import AgencyDBWriter
from AgencyScreenWriter import AgencyScreenWriter


class AgencyScraper(object):
    def __init__(self, writer=None):
        if writer is None:
            writer = AgencyScreenWriter
        self.writer = writer

    @classmethod
    def createForDBOutput(cls):
        return cls(AgencyDBWriter)

    @classmethod
    def createForScreenOutput(cls):
        return cls(AgencyScreenWriter)
