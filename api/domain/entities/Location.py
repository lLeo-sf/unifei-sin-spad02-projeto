from typing import Optional
from api.domain.entities.BaseEntity import BaseEntity


class Location(BaseEntity):
    def __init__(
        self,
        city: Optional[str] = None,
        citystate: Optional[str] = None,
        coordinates: Optional[str] = None,
        country: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        phoneExt: Optional[str] = None,
        postalcode: Optional[str] = None,
        postalcodePlus4: Optional[str] = None,
        state: Optional[str] = None,
        street: Optional[str] = None,
        url: Optional[str] = None
    ):
        self.__dict__.update(locals())
        del self.self
