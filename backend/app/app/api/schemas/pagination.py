from typing import Optional, List, Any
from abc import ABC
from pydantic import BaseModel


class Pagination(BaseModel):  # todo: figure out which onse are not optional
    current_page: Optional[int]
    first_item: Optional[int]
    last_item: Optional[int]
    first_page: Optional[int]
    last_page: Optional[int]
    previous_page: Optional[int]
    next_page: Optional[int]
    items_per_page: Optional[int]
    total_number_of_items: Optional[int]
    number_of_pages: Optional[int]


class PaginatedModel(BaseModel, ABC):
    """
    Paginated model abstraction.

    Example -> UsersPaginated
    """
    items: List[Any]
    pagination: Pagination
    class Meta: orm_model_class = None

    @classmethod
    def from_paginated_query(cls, paginated_query):
        if not cls.Meta.orm_model_class:
            raise NotImplementedError(f'{cls.__name__}.Meta.orm_model_class attr not found!')

        return cls(
            items=[cls.Meta.orm_model_class(**item.__dict__) for item in paginated_query.items],
            pagination=Pagination(
                current_page=paginated_query.page,
                first_item=paginated_query.first_item,
                last_item=paginated_query.last_item,
                first_page=paginated_query.first_page,
                last_page=paginated_query.last_page,
                previous_page=paginated_query.previous_page,
                next_page=paginated_query.next_page,
                items_per_page=paginated_query.items_per_page,
                total_number_of_items=len(paginated_query.items),
                number_of_pages=paginated_query.page_count
            )
        )
