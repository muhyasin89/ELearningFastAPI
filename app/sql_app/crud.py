from sqlalchemy.orm import Session

from .models import Package as Package_Model
from .schema import PackageCreate


def create_package(db: Session, packages: PackageCreate):

    db_package = Package_Model(
        package=packages.package,
        version=packages.version,
        depends=packages.depends,
        suggests=packages.suggests,
        imports=packages.imports,
        license=packages.license,
        MD5sum=packages.MD5sum,
        NeedsCompilation=packages.NeedsCompilation,
    )
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    return db_package
