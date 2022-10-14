import uvicorn


if __name__ == "__main__":
    uvicorn.run("allocation.entrypoints.fastapi_app:app", reload=True)