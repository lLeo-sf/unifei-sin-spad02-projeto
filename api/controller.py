from typing import Any, Dict, List
from fastapi import APIRouter, Body, Depends, HTTPException
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

        result[table_name] = {"base": base_fields, "relations": relations}

    return result

@router.post(
    "/search",
    response_model=List[Dict[str, Any]],
    summary="Executa consulta Ad Hoc e retorna lista de mapas dinâmicos"
)
def search(
    request_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    raw = generate_dynamic_query(request_data, db)

    # monta cols usando exatamente os aliases que o SELECT produziu
    if request_data.get("aggregations"):
        cols: List[str] = []
        # 1) todas as colunas de grouping (ex: "Animals.agegroup")
        cols.extend(request_data.get("grouping", []))
        # 2) cada função + campo, ex: "count.Animals.id"
        cols.extend([
            f"{agg['function']}.{agg['field']}"
            for agg in request_data["aggregations"]
        ])
    else:
        cols = request_data.get("columns", [])

    try:
        return render_adhoc_query_response(raw, cols)
    except Exception as e:
        raise HTTPException(500, detail=str(e))