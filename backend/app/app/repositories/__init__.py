from abc import ABC
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.orm import Query
from paginate_sqlalchemy import SqlalchemyOrmPage

from app.errors.repository import InvalidQueryLimitError, InvalidOrderByError, EntityNotFoundError, TransactionError

# todo: up ver -> sqlalchemy, pydantic !!!


class Paginated(SqlalchemyOrmPage): pass  # https://github.com/Pylons/paginate_sqlalchemy


class Repository(ABC):
    """
    Repository abstraction.

    todo: example usage
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

    def get(self, entity_id: int, ignore_not_found: bool = False):  # todo: check return type in alchemy docs
        entity = self.session.query(self.entity).get(entity_id)
        if not entity and not ignore_not_found:
            raise EntityNotFoundError(f'{self.entity.__name__}[id: {entity_id}] not found.')
        return entity

    def get_by(self, **kwargs):  # todo: check return type in alchemy docs
        ignore_not_found = kwargs.pop('ignore_not_found', False)
        entity = self.session.query(self.entity).filter_by(**kwargs).first()
        if not entity and not ignore_not_found:
            raise EntityNotFoundError(f'{self.entity.__name__}[{kwargs}] not found.')
        return entity

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
            if '???' in repr(e):  # todo: grab error related to insert
                raise TransactionError(f"Transaction failed: \nException msg: " + repr(e))
            raise e  # re-raise (bug to fix)

    def delete(self, entity_id: int) -> None:
        try:
            self.session.query(self.entity).filter(self.entity.id == entity_id).delete()
            self.session.commit()
        except Exception as e:
            if '???' in repr(e):  # todo: grab error related to delete
                raise TransactionError(f"Transaction failed: \nException msg: " + repr(e))
            raise e  # re-raise (bug to fix)

    def _validate_query_limit(self, limit: int) -> None:
        if limit < 1:
            raise InvalidQueryLimitError(f'Query limit invalid: {limit} when minimum is 1')
        if limit > self.max_query_limit:
            raise InvalidQueryLimitError(f'Query limit invalid: {limit} when max is {self.max_query_limit}')
