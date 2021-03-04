
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, UniqueConstraint, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, validates

import settings

Base = declarative_base()


class Connection:
    @staticmethod
    def connect():
        """
        Establish a connection with the database.

        Returns:
            db_session: a database session.

        """
        database = settings.DATABASE['PATH']
        engine = create_engine(database)
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        db_session = sessionmaker(bind=engine)
        db_session = db_session()
        db_session.execute('pragma foreign_keys=on')
        return db_session


class TrainModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    accuracy = Column(Integer)
    train_date = Column(String)
    serving = Column(Boolean, nullable=False)
    model_params = Column(Text)

    @classmethod
    def add(cls, **kwargs):
        """
        Adds a new item in the database.
        Args:
            **kwargs:
             the collection of arguments necessary to create the desired item.

        Returns:
            new_id: the newly added item id.

        """
        session = Connection.connect()
        new_element = cls(**kwargs)
        session.add(new_element)
        session.commit()
        new_id = new_element.id
        session.close()
        return new_id

    @classmethod
    def get(cls, **kwargs):
        """
        Gets a specific item from the database.

        Args:
            **kwargs:
                id: the to-be-queried item id.

        Returns:
            record: the desired item details.

        """
        session = Connection.connect()
        q = session.query(cls)
        q = q.filter_by(id=kwargs['id'])
        record = q.one()
        session.close()
        return record

    @classmethod
    def query(cls, **kwargs):
        """
        Gets a specific item from the database.

        Args:
            **kwargs:
                id: the to-be-queried item id.

        Returns:
            record: the desired item details.

        """
        session = Connection.connect()
        q = session.query(cls)
        record = q.all()
        session.close()
        return record



