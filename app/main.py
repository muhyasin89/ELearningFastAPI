import json
import os
import tarfile
from typing import List, Optional

import pandas as pd
import uvicorn
import wget
from fastapi import Depends, FastAPI, Request
from sqlalchemy import insert
from sqlalchemy.orm import Session

from . import ROOT_DIR
from .sql_app.crud import create_package
from .sql_app.database import SessionLocal, engine
from .sql_app.models import Base
from .sql_app.models import Package as Package_Model
from .sql_app.schema import Package as Package_Schema
from .sql_app.schema import PackageCreate
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
async def read_root(request: Request, db: Session = Depends(get_db)):
    limit = request.query_params.get("limit")
    insert = request.query_params.get("insert")
    reload = request.query_params.get("reload")

    insert = insert if insert else False
    limit = int(limit) if limit else 0

    result_file = "{}/tmp/result.json".format(ROOT_DIR)
    if reload:
        result = request_cran(limit, insert)

        # to make new file
        tmp_folder = "{}/tmp/".format(ROOT_DIR)
        if not os.path.exists(tmp_folder):
            os.mkdir(tmp_folder)

        if not os.path.isfile(result_file):
            f = open(result_file, "a")
            f.close()

        with open(result_file, "w") as outfile:
            outfile.write(json.dumps(result))

    elif os.path.isfile(result_file):
        f = open(
            result_file,
        )
        result = f.read()
        result = json.loads(result)
        f.close()

    if insert:
        # insert into record
        for item in result["data"]:
            NeedsCompilation = item["NeedsCompilation"]
            NeedsCompilation = (
                True if NeedsCompilation.lower() == "yes" else False
            )
            packages = PackageCreate(
                package=item["Package"],
                version=item["Version"],
                depends=item["Depends"] if "Depends" in item else "",
                suggests=item["Suggests"] if "Suggests" in item else "",
                imports=item["Imports"] if "Imports" in item else "",
                license=item["License"] if "License" in item else "",
                MD5sum=item["MD5sum"],
                NeedsCompilation=NeedsCompilation,
            )
            create_package(db=db, packages=packages)

    return result


@app.get("/packages/", response_model=List[Package_Schema])
async def show_records(db: Session = Depends(get_db)):
    records = db.query(Package_Model).all()
    return records


@app.get("/packages/{package_name}/{package_version}/")
async def read_item(
    package_name: str, package_version: str, q: Optional[str] = None
):
    file = "{}/tmp/{}_{}.tar.gz".format(ROOT_DIR, package_name, package_version)
    message = "success"
    if not os.path.exists(file):
        wget.download(
            "http://cran.rproject.org/src/contrib/{}_{}.tar.gz".format(
                package_name, package_version
            ),
            ROOT_DIR + "/tmp",
        )

    tmp_folder = "{}/tmp/".format(ROOT_DIR)
    to_destination = "{}/tmp/{}".format(ROOT_DIR, package_name)
    if not os.path.exists(to_destination):
        os.mkdir(to_destination)

    if file.endswith("tar.gz"):
        try:
            my_tar = tarfile.open(file)
            my_tar.extract(file, to_destination)
            my_tar.close()
        except:
            message = "file could not be opened successfully"

    return {
        "package_name": package_name,
        "package_version": package_version,
        "q": q if q else "",
        "message": message,
    }


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST"), port=os.getenv("PORT"))
