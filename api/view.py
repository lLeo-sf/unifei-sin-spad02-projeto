from typing import List, Tuple
from schemas import AdhocQueryResponse

def render_adhoc_query_response(results: List[Tuple], columns: List[str]) -> AdhocQueryResponse:
    response = []
    for row in results:
        if not isinstance(row, tuple):
            row = (row,)
        row_dict = {columns[idx]: row[idx] for idx in range(len(columns))}
        response.append(row_dict)
    return AdhocQueryResponse(__root__=response)