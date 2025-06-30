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
            if "." in col:
                # formato Tabela.campo
                _, field = col.split(".", 1)
                value = row.get(field)
                if value is None:
                    # tenta achar agregação: ex. min_field, avg_field etc.
                    suffix = f"_{field}"
                    for k, v in row.items():
                        if k.endswith(suffix):
                            value = v
                            break
            else:
                # rótulo simples (ex: "min_id")
                value = row.get(col)
            new_row[col] = value
        output.append(new_row)
    return output