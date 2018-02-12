""" Data layer for Asset Allocation """
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, REAL, DateTime, ForeignKey

Base = declarative_base()


class AssetClass(Base):
    __tablename__ = 'AssetClass'

    id = Column(Integer, primary_key=True)
    parentid = Column(Integer)
    name = Column(String(255), unique=True, nullable=False)
    allocation = Column(REAL)
    sortorder = Column(Integer)
    diff_adjustment = Column(REAL)

    def __repr__(self):
        return "<Tag (name='%s')>" % (self.name)


class AssetClassStock(Base):
    """ Link between Asset Class and stocks """
    __tablename__ = 'AssetClass_Stock'

    id = Column(Integer, primary_key=True)
    assetclassid = Column(Integer)
    symbol = Column(String(50))

    def __repr__(self):
        return "<AssetClass_Stock (assetclass=%s, symbol='%s')>" % (self.assetclassid, self.symbol)


def get_session() -> sessionmaker:
    # connection
    engine = create_engine('sqlite://data/asset_allocation.db')

    # create metadata (?)
    Base.metadata.create_all(engine)

    # create session
    Session = sessionmaker(bind=engine)
    session = Session()

    return session
