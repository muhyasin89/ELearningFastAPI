from datetime import date

from pydantic import BaseModel


class PackageBase(BaseModel):
    package: str
    version: str
    imports: str
    suggests: str
    depends: str
    license: str
    MD5sum: str
    NeedsCompilation: bool


class PackageCreate(PackageBase):
    pass


class Package(PackageBase):
    id: int

    class Config:
        orm_mode = True
