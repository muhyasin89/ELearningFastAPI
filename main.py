import json
import os
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request

from utils import request_cran

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/package/")
async def read_root(request: Request):
    limit = request.query_params.get("limit")
    insert = request.query_params.get("insert")

    insert = insert if insert else False
    limit = int(limit) if limit else 0

    list_cran = request_cran()

    result = {
        "limit": limit,
        "insert": insert,
        "data": list_cran[:limit] if limit else list_cran,
    }

    return result


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST"), port=os.getenv("PORT"))
