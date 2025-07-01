from pydantic import BaseModel
from pydantic import RootModel
from typing import List, Dict, Any, Literal, Optional

class Aggregation(BaseModel):
    function: Literal['avg', 'min', 'max', 'count']
    field: str
class FilterItem(BaseModel):
    field: str
    operator: Literal['=', '!=', '>', '>=', '<', '<=', 'in', 'not_in', 'like']
    value: Any
    
class SortItem(BaseModel):
    column: str
    direction: Literal['asc', 'desc'] = 'asc'
    
class AdhocQueryRequest(BaseModel):
    table: str
    columns: Optional[List[str]] = None
    filters: Optional[List[FilterItem]] = None
    grouping: Optional[List[str]] = None
    aggregations: Optional[List[Aggregation]] = None
    order_by: Optional[List[SortItem]] = None

class AdhocQueryResponse(RootModel[List[Dict[str, Any]]]):
    pass
