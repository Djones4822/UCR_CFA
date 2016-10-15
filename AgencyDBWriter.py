from sqlalchemy.orm import sessionmaker


class AgencyDBWriter(object):

    def __init__(self, sa_engine):
        DBsession = sessionmaker(bind=sa_engine)

        self.session = DBsession()
