from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from allocation.adapters import orm
from allocation.domain import model

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class AbstractProductRepository(ABC):
    def __init__(self):
        self.seen = set()  # type: set[model.Product]

    def add(self, product: model.Product):
        self._add(product)
        self.seen.add(product)

    def get(self, sku: str) -> model.Product:
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product

    def get_by_batchref(self, batchref: str) -> model.Product:
        product = self._get_by_batchref(batchref)
        if product:
            self.seen.add(product)
        return product

    @abstractmethod
    def _add(self, product: model.Product): ...

    @abstractmethod
    def _get(self, sku: str) -> model.Product: ...

    @abstractmethod
    def _get_by_batchref(self, batchref: str) -> model.Product: ...


class SqlAlchemyProductRepository(AbstractProductRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def _add(self, product: model.Product):
        self.session.add(product)

    def _get(self, sku: str) -> model.Product:
        return (
            self.session.query(model.Product).filter_by(sku=sku).one_or_none()
        )

    def _get_by_batchref(self, batchref: str) -> model.Product:
        return (
            self.session.query(model.Product)
            .join(model.Batch)
            .filter(orm.batches.c.reference == batchref)
            .one_or_none()
        )


# avoid raw sql in handlers.py
class SqlAlchemyViewRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_allocation_by_orderid(self, orderid: str):
        return self.session.query(
            orm.allocations_view.c.sku,
            orm.allocations_view.c.batchref,
        ).filter_by(orderid=orderid).all()  

    def add_allocation_to_view(self, orderid: str, sku: str, batchref: str):
        self.session.execute(
            orm.allocations_view.insert().values(
                orderid=orderid,
                sku=sku,
                batchref=batchref,
            ),
        )
    
    def delete_allocation_from_view(self, orderid: str, sku: str):
        self.session.query(orm.allocations_view).filter_by(
            orderid=orderid,
            sku=sku,
        ).delete()