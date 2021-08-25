import json
import os
from typing import List

import uvicorn
from fastapi import Depends, FastAPI, Request
from sqlalchemy.orm import Session

from . import ROOT_DIR
from .sql_app.database import SessionLocal, engine
from .sql_app.models import Base
from .sql_app.models import Package as Package_Model
from .sql_app.schema import Package as Package_Schema
from .utils import request_cran

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/package/get/data")
async def read_root(request: Request):
    limit = request.query_params.get("limit")
    insert = request.query_params.get("insert")
    reload = request.query_params.get("reload")

    insert = insert if insert else False
    limit = int(limit) if limit else 0

    if os.path.isfile("{}/tmp/result.json".format(ROOT_DIR)):
        f = open(
            "{}/tmp/result.json".format(ROOT_DIR),
        )
        result = f.read()
        result = json.loads(result)
        f.close()
    else:
        list_cran = request_cran()
        result = {
            "limit": limit,
            "insert": insert,
            "data": list_cran[: (limit + 1)] if limit else list_cran,
        }

    if reload:
        if not os.path.exists("{}/tmp/".format(ROOT_DIR)):
            os.mkdir("{}/tmp/".format(ROOT_DIR))

        if not os.path.isfile("{}/tmp/result.json".format(ROOT_DIR)):
            f = open("{}/tmp/result.json".format(ROOT_DIR), "a")
            f.close()

        with open("{}/tmp/result.json".format(ROOT_DIR), "w") as outfile:
            outfile.write(json.dumps(result))
    return result


@app.get("/packages/", response_model=List[Package_Schema])
def show_records(db: Session = Depends(get_db)):
    records = db.query(Package_Model).all()
    return records


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST"), port=os.getenv("PORT"))
