from pydantic import BaseModel
from pydantic import RootModel
from typing import List, Dict, Any, Literal, Optional

class Aggregation(BaseModel):
    function: Literal['avg', 'min', 'max']
    field: str
    
class AdhocQueryRequest(BaseModel):
    table: str
    columns: Optional[List[str]] = None
    filters: Optional[Dict[str, List[str]]] = None
    grouping: Optional[List[str]] = None
    aggregations: Optional[List[Aggregation]] = None

class AdhocQueryResponse(RootModel[List[Dict[str, Any]]]):
    pass
