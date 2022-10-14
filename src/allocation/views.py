from allocation.service_layer import unit_of_work


def allocations(
    orderid: str,
    uow: unit_of_work.SqlAlchemyUnitOfWork
) -> list[dict[str, str]]:
    with uow:
        results = uow.views.get_allocation_by_orderid(orderid)
        # results = uow.session.execute(
        #     "SELECT sku, batchref FROM allocations_view"
        #     "\nWHERE orderid = :orderid",
        #     dict(orderid=orderid),
        # )  
    return [dict(r) for r in results]

