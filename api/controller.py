
from fastapi import APIRouter, Depends
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
    metadata = {}
    for table_name, model in TABLE_MODELS.items():
        columns = [c.key for c in model.__table__.columns]
        metadata[table_name] = columns
    return metadata

@router.post("/search", response_model=AdhocQueryResponse)
def search(request: AdhocQueryRequest, db: Session = Depends(get_db)):
    raw_results = generate_dynamic_query(request, db)
    return render_adhoc_query_response(raw_results, request.columns)
