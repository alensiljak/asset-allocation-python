"""
Data layer for Asset Allocation 
Examples:
- insert
    item = new AssetClass()
    session.add(item)
- edit:
    loaded = session.query(dal.AssetClass).filter(dal.AssetClass.name == "test-updated").first()
    loaded.name = "test-updated"
- delete
    loaded = session.query(dal.AssetClass).filter(dal.AssetClass.name == "test-updated").first()
    session.delete(loaded)
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Table, Column, Integer, String, REAL, DateTime, ForeignKey
from asset_allocation.config import Config, ConfigKeys

Base = declarative_base()


class AssetClass(Base):
    __tablename__ = 'AssetClass'

    id = Column(Integer, primary_key=True)
    parentid = Column(Integer)
    name = Column(String(255), unique=True, nullable=False)
    allocation = Column(REAL)
    sortorder = Column(Integer)
    diff_adjustment = Column(REAL)

    stock_links = relationship('AssetClassStock', backref="assetclass", lazy='dynamic') 
    #, cascade = "all,delete")

    def __repr__(self):
        return "<Tag (name='%s')>" % (self.name)


class AssetClassStock(Base):
    """ Link between Asset Class and stocks """
    __tablename__ = 'AssetClass_Stock'

    id = Column(Integer, primary_key=True)
    assetclassid = Column(Integer, ForeignKey("AssetClass.id"))
    symbol = Column(String(50))

    def __repr__(self):
        return "<AssetClass_Stock (assetclass=%s, symbol='%s')>" % (self.assetclassid, self.symbol)


def get_session():
    cfg = Config()
    db_path = cfg.get(ConfigKeys.asset_allocation_database_path)

    # connection
    con_str = "sqlite:///" + db_path
    # Display all SQLite info with echo.
    engine = create_engine(con_str, echo=True)

    # create metadata (?)
    Base.metadata.create_all(engine)

    # create session
    Session = sessionmaker(bind=engine)
    session = Session()

    return session
