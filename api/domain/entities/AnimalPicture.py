from typing import Optional
from api.domain.entities.BaseEntity import BaseEntity

class AnimalPicture(BaseEntity):
    def __init__(
        self,
        created: Optional[str] = None,
        large: Optional[str] = None,
        order: Optional[int] = None,
        original: Optional[str] = None,
        small: Optional[str] = None,
        updated: Optional[str] = None
    ):
        self.__dict__.update(locals())
        del self.self
