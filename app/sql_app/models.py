from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    package = Column(String)
    version = Column(String)
    imports = Column(String)
    suggests = Column(String)
    depends = Column(String)
    license = Column(String)
    MD5sum = Column(String)
    NeedsCompilation = Column(Boolean, default=False)

    details = relationship("Detail", back_populates="packages", uselist=False)

    package_authors = relationship(
        "PackageAuthor", back_populates="packages", uselist=False
    )

    def __repr__(self):
        return "<Package(package='%s', version='%s', license='%s')>" % (
            self.package,
            self.version,
            self.license,
        )


class PackageAuthor(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)

    packages_id = Column(Integer, ForeignKey("packages.id"))
    packages = relationship(
        "Package", back_populates="package_authors", uselist=False
    )


class Detail(Base):
    __tablename__ = "details"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    title = Column(String)
    author = Column(String)
    maintainer = Column(String)
    depends = Column(String)
    description = Column(String)
    repository = Column(String)

    packages_id = Column(Integer, ForeignKey("packages.id"))
    packages = relationship("Package", back_populates="details", uselist=False)

    def __repr__(self):
        return "<Detail(title='%s', author='%s', maintainer='%s')>" % (
            self.title,
            self.author,
            self.maintainer,
        )
