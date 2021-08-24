from datetime import date

from pydantic import BaseModel


class Package(BaseModel):
    id: int
    package: str
    version: str
    name: str
    imports: str
    license: str
    MD5sum: str
    NeedsCompilation: bool
    email: str
    name: str

    class Config:
        orm_mode = True
