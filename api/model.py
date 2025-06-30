from typing import Any, List, Dict
from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String, Text, Tuple, create_engine, func, select
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
    __tablename__ = 'organizations'

    id                          = Column(Integer, primary_key=True)
    about                       = Column(Text)
    adoptionProcess             = Column(Text)
    adoptionUrl                 = Column(Text)
    city                        = Column(Text)
    citystate                   = Column(Text)
    coordinates                 = Column(Text)
    country                     = Column(Text)
    donationUrl                 = Column(Text)
    email                       = Column(Text)
    facebookUrl                 = Column(Text)
    isCommonapplicationAccepted = Column(Boolean)
    lat                         = Column(Float)
    lon                         = Column(Float)
    name                        = Column(Text)
    phone                       = Column(Text)
    serveAreas                  = Column(Text)
    services                    = Column(Text)
    sponsorshipUrl              = Column(Text)
    state                       = Column(Text)
    street                      = Column(Text)
    type                        = Column(Text)
    url                         = Column(Text)

    animals = relationship('Animal', back_populates='organization')


class Species(Base):
    __tablename__ = 'species'

    id            = Column(Integer, primary_key=True)
    plural        = Column(Text)
    singular      = Column(Text)
    youngPlural   = Column(Text)
    youngSingular = Column(Text)

    animals = relationship('Animal', back_populates='species')


class Pattern(Base):
    __tablename__ = 'patterns'

    id   = Column(Integer, primary_key=True)
    name = Column(Text)

    animals = relationship('Animal', back_populates='pattern')


class Breed(Base):
    __tablename__ = 'breeds'

    id   = Column(Integer, primary_key=True)
    name = Column(Text)

    animals_primary = relationship(
        'Animal',
        back_populates='breedPrimaryRel',
        foreign_keys='Animal.breedPrimaryId'
    )
    animals_secondary = relationship(
        'Animal',
        back_populates='breedSecondaryRel',
        foreign_keys='Animal.breedSecondaryId'
    )


class Status(Base):
    __tablename__ = 'statuses'

    id          = Column(Integer, primary_key=True)
    name        = Column(Text)
    description = Column(Text)

    animals = relationship('Animal', back_populates='status')


class Location(Base):
    __tablename__ = 'locations'

    id              = Column(Integer, primary_key=True)
    city            = Column(Text)
    citystate       = Column(Text)
    coordinates     = Column(Text)
    country         = Column(Text)
    lat             = Column(Float)
    lon             = Column(Float)
    name            = Column(Text)
    phone           = Column(Text)
    phoneExt        = Column(Text)
    postalCode      = Column(Text)
    postalCodePlus4 = Column(Text)
    state           = Column(Text)
    street          = Column(Text)
    url             = Column(Text)


class Animal(Base):
    __tablename__ = 'animals'

    id                   = Column(Integer, primary_key=True)
    name                 = Column(Text)
    speciesId            = Column('speciesid', Integer, ForeignKey('species.id'))
    breedPrimaryId       = Column('breedprimaryid', Integer, ForeignKey('breeds.id'))
    breedSecondaryId     = Column('breedsecondaryid', Integer, ForeignKey('breeds.id'))
    patternId            = Column('patternid', Integer, ForeignKey('patterns.id'))
    statusId             = Column('statusid', Integer, ForeignKey('statuses.id'))
    organizationId       = Column('organizationid', Integer, ForeignKey('organizations.id'))
    activityLevel        = Column(Text)
    adoptedDate          = Column(Date)
    ageGroup             = Column(Text)
    availableDate        = Column(Date)
    coatLength           = Column(Text)
    colorDetails         = Column(Text)
    createdDate          = Column(Date)
    energyLevel          = Column(Text)
    fenceNeeds           = Column(Text)
    foundDate            = Column(Date)
    foundPostalcode      = Column(Text)
    indoorOutdoor        = Column(Text)
    isAdoptionPending    = Column(Boolean)
    isBreedMixed         = Column(Boolean)
    isCatsOk             = Column(Boolean)
    isCurrentVaccinations= Column(Boolean)
    isDogsOk             = Column(Boolean)
    isHousetrained       = Column(Boolean)
    isKidsOk             = Column(Boolean)
    isNeedingFoster      = Column(Boolean)
    isSpecialNeeds       = Column(Boolean)
    isSponsorable        = Column(Boolean)
    isYardRequired       = Column(Boolean)
    newPeopleReaction    = Column(Text)
    obedienceTraining    = Column(Text)
    priority             = Column(Text)
    rescueId             = Column(Text)
    sex                  = Column(Text)
    sizeGroup            = Column(Text)
    specialNeedsDetails  = Column(Text)
    sponsorshipMinimum   = Column(Text)
    updatedDate          = Column(Date)

    species          = relationship('Species', back_populates='animals')
    pattern          = relationship('Pattern', back_populates='animals')
    status           = relationship('Status', back_populates='animals')
    organization     = relationship('Organization', back_populates='animals')
    breedPrimaryRel  = relationship(
        'Breed',
        back_populates='animals_primary',
        foreign_keys=[breedPrimaryId]
    )
    breedSecondaryRel= relationship(
        'Breed',
        back_populates='animals_secondary',
        foreign_keys=[breedSecondaryId]
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
    "Organizations": Organization
}

def get_column(model, column_name):
    try:
        return getattr(model, column_name)
    except AttributeError:
        raise ValueError(f"Column {column_name} not found in model {model.__name__}")

def generate_dynamic_query(request: AdhocQueryRequest, db: Session) -> List[Dict[str, Any]]:
    table_name = request.table
    columns    = request.columns or []
    grouping   = list(request.grouping or [])
    filters    = request.filters or {}

    Model = TABLE_MODELS[table_name]

    # Se agregações estão pedidas, ignore-as no grouping para não causar GROUP BY nelas
    agg_fields = [agg.field for agg in (request.aggregations or [])]
    grouping = [g for g in grouping if g not in agg_fields]

    # Monta colunas simples
    select_expressions = [
        getattr(TABLE_MODELS[tbl], field).label(field)
        for col in columns
        for tbl, field in [col.split('.')]
    ]

    # Monta agregações (AVG, MIN, MAX)
    for agg in request.aggregations or []:
        tbl, field = agg.field.split('.')
        cls = TABLE_MODELS[tbl]
        fn = getattr(func, agg.function)
        select_expressions.append(fn(getattr(cls, field)).label(f"{agg.function}_{field}"))

    # Se há agregações mas não sobrou nenhum grouping válido, não faz GROUP BY
    stmt = select(*select_expressions).select_from(Model)

    # Aplica possíveis joins
    for col in columns:
        tbl, _ = col.split('.')
        if tbl != table_name:
            stmt = stmt.join(TABLE_MODELS[tbl])

    # Aplica filtros
    for col, vals in filters.items():
        tbl, field = col.split('.')
        stmt = stmt.where(getattr(TABLE_MODELS[tbl], field).in_(vals))

    # Aplica agrupamento somente se ainda houver campos
    if grouping:
        group_exprs = [
            getattr(TABLE_MODELS[tbl], field)
            for grp in grouping
            for tbl, field in [grp.split('.')]
        ]
        stmt = stmt.group_by(*group_exprs)

    result = db.execute(stmt).mappings().all()
    return [dict(row) for row in result]
