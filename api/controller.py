
from fastapi import APIRouter, Depends
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from schemas import AdhocQueryRequest, AdhocQueryResponse
from view import render_adhoc_query_response
from model import SessionLocal
from model import TABLE_MODELS
from model import generate_dynamic_query

router = APIRouter()

def get_db():
    db = SessionLocal()  
    try:
        yield db          
    finally:
        db.close() 

@router.get("/metadata")
def metadata():
    result = {}
    for table_name, model in TABLE_MODELS.items():
        mapper = inspect(model)

        # campos "base"
        base_fields = [col.key for col in mapper.columns]

        # campos de "relations"
        relations = {}
        for rel in mapper.relationships:
            related_cls = rel.mapper.class_
            related_table = related_cls.__tablename__  # e.g. "Organizations", "Breeds"…
            # lista todas as colunas da tabela relacionada
            related_columns = [c.name for c in related_cls.__table__.columns]
            relations[related_table] = related_columns

        result[table_name] = {
            "base": base_fields,
            "relations": relations
        }

    return result

@router.post("/search", response_model=AdhocQueryResponse)
def search(request: AdhocQueryRequest, db: Session = Depends(get_db)):
    raw_results = generate_dynamic_query (request, db)
    return render_adhoc_query_response(raw_results, request.columns)
