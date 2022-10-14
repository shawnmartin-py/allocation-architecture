from fastapi import FastAPI, HTTPException, status

from allocation.domain import commands
from allocation.service_layer.handlers import InvalidSku
from allocation import bootstrap, views


app = FastAPI()
bus = bootstrap.bootstrap()


@app.post("/batches", status_code=status.HTTP_201_CREATED)
def add_batch(cmd: commands.CreateBatch):
    bus.handle(cmd)
    return "OK"


@app.post("/allocate", status_code=status.HTTP_202_ACCEPTED)
def allocate_endpoint(cmd: commands.Allocate):
    try:
        bus.handle(cmd)
    except InvalidSku as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
    return "OK"


@app.get("/allocations/{orderid}")
def allocation_view_endpoint(orderid: str):
    result = views.allocations(orderid, bus.uow)
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")
    return result