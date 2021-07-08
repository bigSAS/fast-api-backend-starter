from abc import ABC
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.orm import Query
from paginate_sqlalchemy import SqlalchemyOrmPage

from app.errors.repository import InvalidQueryLimitError, InvalidOrderByError, EntityNotFoundError, TransactionError
from app.database.setup import Base as Entity

# todo: up ver -> sqlalchemy, pydantic !!!
# todo: adapt fiql in repository ?


class Paginated(SqlalchemyOrmPage): pass  # https://github.com/Pylons/paginate_sqlalchemy


class Repository(ABC):
    """
    Repository abstraction.

    examples in repositories.users, repositories.permissions
    """
    entity = NotImplemented
    max_query_limit = 100

    def __init__(self, db_session: Session):
        if not self.entity:
            raise NotImplementedError(f'{self.__class__.__name__}.entity not set!')
        self._db_session = db_session

    @property
    def session(self) -> Session:
        return self._db_session

    def get_by(self, **kwargs) -> Optional[Entity]:
        """
        Gets object by filters.
        Filters must be bassed using kwargs and mach Entity attributes.

        ex.
        repo.get_by(name=foo, email=bar, ignore_not_found=True)
        repo.get_by(name=foo, email=bar)
        repo.get_by(id=1)
        repo.get(1) - proxy for id
        repo.get(1, ignore_not_found=True) - proxy for id ignoring not found

        When ignore_not_found=True - returns None when object is not found
        When ignore_not_found=True - raises EntityNotFoundError when object is not found
        """
        ignore_not_found = kwargs.pop('ignore_not_found', False)
        entity = self.session.query(self.entity).filter_by(**kwargs).first()
        if not entity and not ignore_not_found:
            raise EntityNotFoundError(f'{self.entity.__name__}[{kwargs}] not found.')
        return entity

    def get(self, entity_id: int, ignore_not_found: bool = False) -> Optional[Entity]:
        return self.get_by(id=entity_id, ignore_not_found=ignore_not_found)

    def all(self, order: str = None) -> Query:
        if order: return self.session.query(self.entity).order_by(text(order)).all()
        return self.session.query(self.entity).all()

    def all_paginated(self, page: int = 1, limit: int = 10, order: str = None) -> Paginated:
        self._validate_query_limit(limit)
        q = self.session.query(self.entity)
        if order:
            if '-' in order:
                order = order.replace('-', '')
                order = f'{order} DESC'
            q = q.order_by(text(order))
        try:
            return Paginated(q, page=page, items_per_page=limit, db_session=self.session)
        except Exception as e:
            if 'psycopg2.errors.UndefinedColumn' in repr(e):
                raise InvalidOrderByError(f"Ivalid order_by column value: {order}\nException msg: " + repr(e))
            raise e  # re-raise (bug to fix)

    def filter(self, f, order: str = None) -> Query:
        if order: return self.session.query(self.entity).filter(f).order_by(text(order)).all()
        return self.session.query(self.entity).filter(f).all()

    def filter_paginated(self, f, page: int = 1, limit: int = 10, order: str = None) -> Paginated:
        self._validate_query_limit(limit)
        q = self.session.query(self.entity).filter(f)
        if order:
            if '-' in order:
                order = order.replace('-', '')
                order = f'{order} DESC'
            q = q.order_by(text(order))
        try:
            return Paginated(q, page=page, items_per_page=limit, db_session=self.session)
        except Exception as e:
            if 'psycopg2.errors.UndefinedColumn' in repr(e):
                raise InvalidOrderByError(f"Ivalid order_by column value: {order}\nException msg: " + repr(e))
            raise e  # re-raise (bug to fix)

    def save(self, entity) -> None:
        try:
            self.session.add(entity)
            self.session.commit()
        except Exception as e:
            raise TransactionError(f"Transaction failed: \nException msg: " + repr(e))

    def delete(self, entity_id: int) -> None:
        obj = self.get(entity_id)
        self.session.delete(obj)
        self.session.commit()

    def _validate_query_limit(self, limit: int) -> None:
        if limit < 1:
            raise InvalidQueryLimitError(f'Query limit invalid: {limit} when minimum is 1')
        if limit > self.max_query_limit:
            raise InvalidQueryLimitError(f'Query limit invalid: {limit} when max is {self.max_query_limit}')
