from typing import Optional
from api.domain.entities.BaseEntity import BaseEntity

class Organization(BaseEntity):
    def __init__(
        self,
        about: Optional[str] = None,
        adoptionProcess: Optional[str] = None,
        adoptionUrl: Optional[str] = None,
        city: Optional[str] = None,
        citystate: Optional[str] = None,
        coordinates: Optional[str] = None,
        country: Optional[str] = None,
        distance: Optional[float] = None,
        donationUrl: Optional[str] = None,
        email: Optional[str] = None,
        facebookUrl: Optional[str] = None,
        fax: Optional[str] = None,
        isCommonapplicationAccepted: Optional[bool] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        meetPets: Optional[str] = None,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        postalcode: Optional[str] = None,
        postalcodePlus4: Optional[str] = None,
        serveAreas: Optional[str] = None,
        services: Optional[str] = None,
        sponsorshipUrl: Optional[str] = None,
        state: Optional[str] = None,
        street: Optional[str] = None,
        type: Optional[str] = None,
        url: Optional[str] = None
    ):
        self.__dict__.update(locals())
        del self.self