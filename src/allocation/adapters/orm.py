import logging

import sqlalchemy as sql
from sqlalchemy.orm import mapper, relationship

from allocation.domain import model


logger = logging.getLogger(__name__)

metadata = sql.MetaData()

order_lines = sql.Table(
    "order_lines",
    metadata,
    sql.Column("id", sql.Integer, primary_key=True, autoincrement=True),
    sql.Column("sku", sql.String(255)),
    sql.Column("qty", sql.Integer, nullable=False),
    sql.Column("orderid", sql.String(255)),
)

products = sql.Table(
    "products",
    metadata,
    sql.Column("sku", sql.String(255), primary_key=True),
    sql.Column(
        "version_number",
        sql.Integer,
        nullable=False,
        server_default="0"
    ),
)

batches = sql.Table(
    "batches",
    metadata,
    sql.Column("id", sql.Integer, primary_key=True, autoincrement=True),
    sql.Column("reference", sql.String(255)),
    sql.Column("sku", sql.ForeignKey("products.sku")),
    sql.Column("_purchased_quantity", sql.Integer, nullable=False),
    sql.Column("eta", sql.Date, nullable=True),
)

allocations = sql.Table(
    "allocations",
    metadata,
    sql.Column("id", sql.Integer, primary_key=True, autoincrement=True),
    sql.Column("orderline_id", sql.ForeignKey("order_lines.id")),
    sql.Column("batch_id", sql.ForeignKey("batches.id")),
)

allocations_view = sql.Table(
    "allocations_view",
    metadata,
    sql.Column("orderid", sql.String(255)),
    sql.Column("sku", sql.String(255)),
    sql.Column("batchref", sql.String(255)),
)


def start_mappers():
    logger.debug("Starting mappers")
    lines_mapper = mapper(model.OrderLine, order_lines)
    batches_mapper = mapper(
        model.Batch,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper,
                secondary=allocations,
                collection_class=set,
            )
        },
    )
    mapper(
        model.Product,
        products,
        properties={"batches": relationship(batches_mapper)},
    )


@sql.event.listens_for(model.Product, "load")
def receive_load(product, _):
    product.events = []
