from typing import Any, Dict, List, Tuple
from schemas import AdhocQueryResponse

def render_adhoc_query_response(
    raw_results: List[Dict[str, Any]],
    columns: List[str]
) -> List[Dict[str, Any]]:
    output: List[Dict[str, Any]] = []
    for row in raw_results:
        new_row: Dict[str, Any] = {}
        for col in columns:
            new_row[col] = row.get(col)
        output.append(new_row)
    return output