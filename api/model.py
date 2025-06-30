from typing import Any, List, Dict
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Tuple,
    create_engine,
    func,
    select,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from schemas import AdhocQueryRequest
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:123qwe@localhost:5432/spad02"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    about = Column(Text)
    adoptionprocess = Column("adoptionprocess", Text)
    adoptionurl = Column("adoptionurl", Text)
    city = Column(Text)
    citystate = Column("citystate", Text)
    coordinates = Column(Text)
    country = Column(Text)
    donationurl = Column("donationurl", Text)
    email = Column(Text)
    facebookurl = Column("facebookurl", Text)
    iscommonapplicationaccepted = Column("iscommonapplicationaccepted", Boolean)
    lat = Column(Float)
    lon = Column(Float)
    name = Column(Text)
    phone = Column(Text)
    serveareas = Column("serveareas", Text)
    services = Column(Text)
    sponsorshipurl = Column("sponsorshipurl", Text)
    state = Column(Text)
    street = Column(Text)
    type = Column(Text)
    url = Column(Text)

    animals = relationship("Animal", back_populates="organization")


class Species(Base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True)
    plural = Column(Text)
    singular = Column(Text)
    youngplural = Column("youngplural", Text)
    youngsingular = Column("youngsingular", Text)

    animals = relationship("Animal", back_populates="species")


class Pattern(Base):
    __tablename__ = "patterns"

    id = Column(Integer, primary_key=True)
    name = Column(Text)

    animals = relationship("Animal", back_populates="pattern")


class Breed(Base):
    __tablename__ = "breeds"

    id = Column(Integer, primary_key=True)
    name = Column(Text)

    animals_primary = relationship(
        "Animal", back_populates="breedprimaryrel", foreign_keys="Animal.breedprimaryid"
    )
    animals_secondary = relationship(
        "Animal",
        back_populates="breedsecondaryrel",
        foreign_keys="Animal.breedsecondaryid",
    )


class Status(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)

    animals = relationship("Animal", back_populates="status")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    city = Column(Text)
    citystate = Column("citystate", Text)
    coordinates = Column(Text)
    country = Column(Text)
    lat = Column(Float)
    lon = Column(Float)
    name = Column(Text)
    phone = Column(Text)
    phoneext = Column("phoneext", Text)
    postalcode = Column("postalcode", Text)
    postalcodeplus4 = Column("postalcodeplus4", Text)
    state = Column(Text)
    street = Column(Text)
    url = Column(Text)


class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    speciesid = Column("speciesid", Integer, ForeignKey("species.id"))
    breedprimaryid = Column("breedprimaryid", Integer, ForeignKey("breeds.id"))
    breedsecondaryid = Column("breedsecondaryid", Integer, ForeignKey("breeds.id"))
    patternid = Column("patternid", Integer, ForeignKey("patterns.id"))
    statusid = Column("statusid", Integer, ForeignKey("statuses.id"))
    organizationid = Column("organizationid", Integer, ForeignKey("organizations.id"))
    activitylevel = Column("activitylevel", Text)
    adopteddate = Column("adopteddate", Date)
    agegroup = Column("agegroup", Text)
    availabledate = Column("availabledate", Date)
    coatlength = Column("coatlength", Text)
    colordetails = Column("colordetails", Text)
    createddate = Column("createddate", Date)
    energylevel = Column("energylevel", Text)
    fenceneeds = Column("fenceneeds", Text)
    founddate = Column("founddate", Date)
    foundpostalcode = Column("foundpostalcode", Text)
    indooroutdoor = Column("indooroutdoor", Text)
    isadoptionpending = Column("isadoptionpending", Boolean)
    isbreedmixed = Column("isbreedmixed", Boolean)
    iscatsok = Column("iscatsok", Boolean)
    iscurrentvaccinations = Column("iscurrentvaccinations", Boolean)
    isdogsok = Column("isdogsok", Boolean)
    ishousetrained = Column("ishousetrained", Boolean)
    iskidsok = Column("iskidsok", Boolean)
    isneedingfoster = Column("isneedingfoster", Boolean)
    isspecialneeds = Column("isspecialneeds", Boolean)
    issponsorable = Column("issponsorable", Boolean)
    isyardrequired = Column("isyardrequired", Boolean)
    newpeoplereaction = Column("newpeoplereaction", Text)
    obediencetraining = Column("obediencetraining", Text)
    priority = Column(Text)
    rescueid = Column("rescueid", Text)
    sex = Column(Text)
    sizegroup = Column("sizegroup", Text)
    specialneedsdetails = Column("specialneedsdetails", Text)
    sponsorshipminimum = Column("sponsorshipminimum", Text)
    updateddate = Column("updateddate", Date)

    species = relationship("Species", back_populates="animals")
    pattern = relationship("Pattern", back_populates="animals")
    status = relationship("Status", back_populates="animals")
    organization = relationship("Organization", back_populates="animals")
    breedprimaryrel = relationship(
        "Breed", back_populates="animals_primary", foreign_keys=[breedprimaryid]
    )
    breedsecondaryrel = relationship(
        "Breed", back_populates="animals_secondary", foreign_keys=[breedsecondaryid]
    )


Base.metadata.create_all(bind=engine)

## ---- Adhoc Report Helpers ----
TABLE_MODELS = {
    "Animals": Animal,
    "Species": Species,
    "Statuses": Status,
    "Patterns": Pattern,
    "Breeds": Breed,
    "Locations": Location,
    "Organizations": Organization,
}


def get_column(model, column_name):
    try:
        return getattr(model, column_name)
    except AttributeError:
        raise ValueError(f"Column {column_name} not found in model {model.__name__}")


from typing import Any, Dict, List
from sqlalchemy import select, func
from sqlalchemy.orm import Session


def generate_dynamic_query(
    request: AdhocQueryRequest, db: Session
) -> List[Dict[str, Any]]:
    table_name = request.table
    columns = request.columns or []
    grouping = list(request.grouping or [])
    filters = request.filters or {}

    Model = TABLE_MODELS[table_name]

    # ignorar campos de agregação em grouping para evitar GROUP BY nelas
    agg_fields = [agg.field for agg in (request.aggregations or [])]
    grouping = [g for g in grouping if g not in agg_fields]

    # montar lista de expressões para SELECT
    select_expressions: List[Any] = []
    for col in columns:
        tbl, field = col.split(".")
        cls = TABLE_MODELS[tbl]
        select_expressions.append(getattr(cls, field).label(field))

    # adicionar agregações
    for agg in request.aggregations or []:
        tbl, field = agg.field.split(".")
        cls = TABLE_MODELS[tbl]
        fn = getattr(func, agg.function)
        select_expressions.append(
            fn(getattr(cls, field)).label(f"{agg.function}_{field}")
        )

    # construir statement inicial
    stmt = select(*select_expressions).select_from(Model)

    # aplicar JOINs sem duplicar
    joined_tables = set()
    for col in columns:
        tbl, _ = col.split(".")
        if tbl != table_name and tbl not in joined_tables:
            stmt = stmt.join(TABLE_MODELS[tbl])
            joined_tables.add(tbl)

    # filtros dinâmicos
    for f in request.filters or []:
        tbl, fld = f.field.split(".", 1)
        cls = TABLE_MODELS[tbl]
        col_attr = getattr(cls, fld)
        op = f.operator
        val = f.value

        if op == "=":
            stmt = stmt.where(col_attr == val)
        elif op == "!=":
            stmt = stmt.where(col_attr != val)
        elif op == ">":
            stmt = stmt.where(col_attr > val)
        elif op == ">=":
            stmt = stmt.where(col_attr >= val)
        elif op == "<":
            stmt = stmt.where(col_attr < val)
        elif op == "<=":
            stmt = stmt.where(col_attr <= val)
        elif op == "in":
            stmt = stmt.where(col_attr.in_(val))
        elif op == "not_in":
            stmt = stmt.where(~col_attr.in_(val))
        elif op == "like":
            stmt = stmt.where(col_attr.like(val))
        else:
            raise ValueError(f"Operador inválido: {op}")

    # aplicar GROUP BY, se houver campos restantes
    if grouping:
        group_exprs = []
        for grp in grouping:
            tbl, field = grp.split(".")
            cls = TABLE_MODELS[tbl]
            group_exprs.append(getattr(cls, field))
        stmt = stmt.group_by(*group_exprs)

    # executar e retornar lista de dicts
    result = db.execute(stmt).mappings().all()
    return [dict(row) for row in result]
