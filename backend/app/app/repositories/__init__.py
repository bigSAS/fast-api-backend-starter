from sqlalchemy.orm import Session
from sqlalchemy import text


class ObjectNotFoundError(Exception): pass  # todo: adapt errors package

# todo: refresh knowlege bout queries from cusg backend for child classes


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
            raise ObjectNotFoundError(f'{self.entity.__name__}[id: {entity_id}] not found.')
        return entity

    def get_by(self, **kwargs):
        ignore_not_found = kwargs.pop('ignore_not_found', False)
        entity = self.session.query(self.entity).filter_by(**kwargs).first()
        if not entity and not ignore_not_found:
            raise ObjectNotFoundError(f'{self.entity.__name__}[{kwargs}] not found.')
        return entity

    def all(self, order: str = None):
        if order: return self.session.query(self.entity).order_by(text(order)).all()
        return self.session.query(self.entity).all()

    def all_paginated(self, page: int = 1, limit: int = 10, order: str = None):
        if order: return self.session.query(self.entity).order_by(text(order)).paginate(page, limit, False)
        return self.session.query(self.entity).paginate(page, limit, False)

    def filter(self, f, order: str = None):
        if order: return self.session.query(self.entity).filter(f).order_by(text(order)).all()
        return self.session.query(self.entity).filter(f).all()

    def filter_paginated(self, f, page: int = 1, limit: int = 10, order: str = None):
        if order: return self.session.query(self.entity).filter(f).order_by(text(order)).paginate(page, limit, False)
        return self.session.query(self.entity).filter(f).paginate(page, limit, False)

    def save(self, entity):
        self.session.add(entity)
        self.session.commit()

    def delete(self, entity_id: int):
        self.session.query(self.entity).filter(self.entity.id == entity_id).delete()
        self.session.commit()
