from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    package = Column(String, index=True)
    version = Column(String, index=True)
    imports = Column(String, index=True)
    license = Column(String, index=True)
    MD5sum = Column(String, index=True)
    NeedsCompilation = Column(Boolean, default=False)
    email = Column(String, index=True)
    name = Column(String, index=True)

    details = relationship("Detail", back_populates="packages", uselist=False)

    def __repr__(self):
        return "<Package(package='%s', version='%s', license='%s')>" % (
            self.package,
            self.version,
            self.license,
        )


class Detail(Base):
    __tablename__ = "details"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    maintainer = Column(String, index=True)
    depends = Column(String, index=True)
    description = Column(String, index=True)
    repository = Column(String, index=True)

    packages_id = Column(Integer, ForeignKey("packages.id"))
    packages = relationship("Package", back_populates="details", uselist=False)

    def __repr__(self):
        return "<Detail(title='%s', author='%s', maintainer='%s')>" % (
            self.title,
            self.author,
            self.maintainer,
        )
