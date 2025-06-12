from typing import List
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Tuple, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from schemas import AdhocQueryRequest
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:123qwe@localhost:5432/spad02"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Organization(Base):
    __tablename__ = "Organizations"
    id = Column(Integer, primary_key=True, index=True)
    about = Column(String)
    adoptionProcess = Column(String)
    adoptionUrl = Column(String)
    city = Column(String)
    citystate = Column(String)
    coordinates = Column(String)
    country = Column(String)
    distance = Column(String)
    donationUrl = Column(String)
    email = Column(String)
    facebookUrl = Column(String)
    fax = Column(String)
    isCommonapplicationAccepted = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    meetPets = Column(String)
    name = Column(String)
    phone = Column(String)
    postcode = Column(String)
    postcodePlus4 = Column(String)
    serveAreas = Column(String)
    services = Column(String)
    sponsorshipUrl = Column(String)
    state = Column(String)
    street = Column(String)
    type = Column(String)
    url = Column(String)

class Species(Base):
    __tablename__ = "Species"
    id = Column(Integer, primary_key=True, index=True)
    plural = Column(String)
    singular = Column(String)
    youngPlural = Column(String)
    youngSingular = Column(String)

class Status(Base):
    __tablename__ = "Statuses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

class Pattern(Base):
    __tablename__ = "Patterns"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Breed(Base):
    __tablename__ = "Breeds"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class AnimalPicture(Base):
    __tablename__ = "AnimalPictures"
    id = Column(Integer, primary_key=True, index=True)
    animalId = Column(Integer)
    size = Column(String)
    url = Column(String)

class Contact(Base):
    __tablename__ = "Contacts"
    id = Column(Integer, primary_key=True, index=True)
    animalId = Column(Integer)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    postalcode = Column(String)
    email = Column(String)
    name = Column(String)
    phone = Column(String)

class Location(Base):
    __tablename__ = "Locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    postalcode = Column(String)
    country = Column(String)
    lat = Column(Float)
    lon = Column(Float)

class Animal(Base):
    __tablename__ = "Animals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    speciesId = Column(Integer, ForeignKey("Species.id"))
    breedPrimaryId = Column(Integer, ForeignKey("Breeds.id"))
    breedSecondaryId = Column(Integer, ForeignKey("Breeds.id"))
    patternId = Column(Integer, ForeignKey("Patterns.id"))
    statusId = Column(Integer, ForeignKey("Statuses.id"))
    organizationId = Column(Integer, ForeignKey("Organizations.id"))

    species = relationship("Species")
    breedPrimary = relationship("Breed", foreign_keys=[breedPrimaryId])
    breedSecondary = relationship("Breed", foreign_keys=[breedSecondaryId])
    pattern = relationship("Pattern")
    status = relationship("Status")
    organization = relationship("Organization")
    
Base.metadata.create_all(bind=engine)

## ---- Adhoc Report Helpers ----
TABLE_MODELS = {
    "Animals": Animal,
    "Species": Species,
    "Statuses": Status,
    "Patterns": Pattern,
    "Breeds": Breed,
    "AnimalPictures": AnimalPicture,
    "Contacts": Contact,
    "Locations": Location,
    "Organizations": Organization
}

def get_column(model, column_name):
    try:
        return getattr(model, column_name)
    except AttributeError:
        raise ValueError(f"Column {column_name} not found in model {model.__name__}")

def generate_dynamic_query(request_json: AdhocQueryRequest, db_session: Session) -> List[Tuple]:
    
    table_name = request_json.get("table")
    columns = request_json.get("columns", [])
    grouping = request_json.get("grouping", [])
    filters = request_json.get("filters", {})

    if table_name not in TABLE_MODELS:
        raise ValueError(f"Unknown table: {table_name}")

    base_model = TABLE_MODELS[table_name]

    query = db_session.query()

    orm_columns = []
    joined_models = set()
    for col in columns:
        tbl, colname = col.split(".")
        model = TABLE_MODELS[tbl]
        column_obj = get_column(model, colname)
        orm_columns.append(column_obj)

        if model != base_model:
            joined_models.add(model)

    group_by_columns = []
    for grp in grouping:
        tbl, colname = grp.split(".")
        model = TABLE_MODELS[tbl]
        column_obj = get_column(model, colname)
        group_by_columns.append(column_obj)

        if model != base_model:
            joined_models.add(model)

    query = db_session.query(*orm_columns)

    # Faz os joins necessarios
    from sqlalchemy.orm import joinedload

    for model in joined_models:
        
        relationship_name = None

        for rel in base_model.__mapper__.relationships:
            if rel.mapper.class_ == model:
                relationship_name = rel.key
                break

        if relationship_name is None:
            raise ValueError(f"Cannot determine relationship from {base_model.__name__} to {model.__name__}")

        query = query.join(getattr(base_model, relationship_name))

    # Aplica os filtros
    from sqlalchemy import or_

    for filter_field, filter_values in filters.items():
        if filter_field not in TABLE_MODELS:
            raise ValueError(f"Unknown filter table: {filter_field}")

        model = TABLE_MODELS[filter_field]
        column_obj = get_column(model, "name")
        query = query.filter(column_obj.in_(filter_values))

        if model != base_model:
            joined_models.add(model)

    # Group by se houver
    if group_by_columns:
        query = query.group_by(*group_by_columns)

    results = query.all()

    return results 
