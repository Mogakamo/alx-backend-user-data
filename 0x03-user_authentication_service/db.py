#!/usr/bin/env python3
""" DB Module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """
    DB Class
    """

    def __init__(self) -> None:
        """ Initialize a database instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

        @property
        def _session(self) -> Session:
            """ Memoized session object
            """
            if self.__session is None:
                DBSession = sessionmaker(bind=self._engine)
                self.__session = DBSession()
            return self.__session

        def add_user(self, email: str, hashed_password: str) -> User:
            """ Add users to the database"""
            new = User(email=email, hashed_password=hashed_password)
            self._session.add(new)
            self._session.commit()
            return new

        def find_user_by(self, **kwargs) -> User:
            """Return the first row found in the users table based on tkeyword args"""

            try:
                record = self._session.query(User).filter_by(**kwargs).first()
            except TypeError:
                raise InvalidRequestError
            if record is None:
                raise NoResultFound
            return record

        def update_user(self, user_id: int, **kwargs) -> User:
            """ Updates Users"""
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError
            self._session.commit()
            return None
