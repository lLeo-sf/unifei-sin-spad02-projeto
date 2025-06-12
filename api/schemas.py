from pydantic import BaseModel
from pydantic import RootModel
from typing import List, Dict, Any

class AdhocQueryRequest(BaseModel):
    table: str
    columns: List[str]
    grouping: List[str] = []
    filters: Dict[str, List[str]] = {}

class AdhocQueryResponse(RootModel[List[Dict[str, Any]]]):
    pass
