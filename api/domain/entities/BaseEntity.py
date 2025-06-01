from typing import Optional, List, Dict, Any
from datetime import datetime

class BaseEntity:
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}