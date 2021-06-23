from sqlalchemy.orm import Session
from sqlalchemy import text
from paginate_sqlalchemy import SqlalchemyOrmPage

from app.errors.api import BadRequestError, NotFoundError


class ObjectNotFoundError(Exception): pass  # todo: adapt errors package


class Paginated(SqlalchemyOrmPage): pass  # https://github.com/Pylons/paginate_sqlalchemy


# usage example in CUSG: https://github.com/bigSAS/critical-usg-backend/blob/master/cusg/events/instruction_documents.py


# todo: refactor pagination as in all_paginated

# todo: up ver -> sqlalchemy, pydantic !!!

# todo: limit max page size -> raise 400

# todo: raise Api errors or raise Repository errors ? sanity tells RepositoryError and handle higher
#  -> (more coding but more SOLID)


class Repository:
    entity = NotImplemented

    def __init__(self, db_session: Session):
        self._db_session = db_session

    @property
    def session(self):
        return self._db_session

    def get(self, entity_id: int, ignore_not_found: bool = False):
        entity = self.session.query(self.entity).get(entity_id)
        if not entity and not ignore_not_found:
            raise NotFoundError(f'{self.entity.__name__}[id: {entity_id}] not found.')
        return entity

    def get_by(self, **kwargs):
        ignore_not_found = kwargs.pop('ignore_not_found', False)
        entity = self.session.query(self.entity).filter_by(**kwargs).first()
        if not entity and not ignore_not_found:
            raise NotFoundError(f'{self.entity.__name__}[{kwargs}] not found.')
        return entity

    def all(self, order: str = None):
        if order: return self.session.query(self.entity).order_by(text(order)).all()
        return self.session.query(self.entity).all()

    def all_paginated(self, page: int = 1, limit: int = 10, order: str = None):
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
                raise BadRequestError(f"Ivalid order_by column value: {order}\nException msg: " + repr(e))
            raise e

    def filter(self, f, order: str = None):
        if order: return self.session.query(self.entity).filter(f).order_by(text(order)).all()
        return self.session.query(self.entity).filter(f).all()

    def filter_paginated(self, f, page: int = 1, limit: int = 10, order: str = None):
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
                raise BadRequestError(f"Ivalid order_by column value: {order}\nException msg: " + repr(e))
            raise e

    def save(self, entity):
        self.session.add(entity)
        self.session.commit()

    def delete(self, entity_id: int):
        self.session.query(self.entity).filter(self.entity.id == entity_id).delete()
        self.session.commit()
