from typing import Any, Dict, List, Tuple
from schemas import AdhocQueryResponse

def render_adhoc_query_response(raw_results: List[Dict[str, Any]], columns: List[str]) -> List[Dict[str, Any]]:
    return raw_results