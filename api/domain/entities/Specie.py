from typing import Optional
from api.domain.entities.BaseEntity import BaseEntity


class Species(BaseEntity):
    def __init__(
        self,
        plural: Optional[str] = None,
        singular: Optional[str] = None,
        youngPlural: Optional[str] = None,
        youngSingular: Optional[str] = None
    ):
        self.__dict__.update(locals())
        del self.self