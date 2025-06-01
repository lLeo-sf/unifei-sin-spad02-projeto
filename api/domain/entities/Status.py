from typing import Optional
from api.domain.entities.BaseEntity import BaseEntity

class Status(BaseEntity):
    def __init__(
        self,
        description: Optional[str] = None,
        name: Optional[str] = None
    ):
        self.description = description
        self.name = name