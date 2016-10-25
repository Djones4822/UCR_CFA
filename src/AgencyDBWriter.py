# Writes agency data to the database
from sqlalchemy.orm import sessionmaker
from Agency import Agency


class AgencyDBWriter(object):
    """
    Used to write agency data to the database
    """

    def __init__(self, sa_engine):
        """
        Create new database writer
        PARAMS:
        sa_engine -- SQL Alchemy Engine to use to connect to DB
        """

        DBsession = sessionmaker(bind=sa_engine)

        self.session = DBsession()

    def write(self, agency_info):
        # For now, turn results into a dict with key = agency name
        # and value = dict with all info. This allows efficent test for
        # membership based on name. Will likely changes as
        # tests for equality become more complex
        self.existing_agencies = {x.__dict__['info']['name']: x.__dict__
                                  for x in self.session.query(Agency).all()}
        for a in agency_info:
            new_agency = Agency(info=a)
            if not self.agency_already_in_db(a):
                self.session.add(new_agency)
        self.session.commit()

    def agency_already_in_db(self, agency_info):
        return agency_info['name'] in self.existing_agencies
