from typing import Optional
from api.domain.entities import BaseEntity


class Contact(BaseEntity):
    def __init__(
        self,
        email: Optional[str] = None,
        firstname: Optional[str] = None,
        fullname: Optional[str] = None,
        lastname: Optional[str] = None,
        name: Optional[str] = None,
        phoneCell: Optional[str] = None,
        phoneHome: Optional[str] = None,
        salutation: Optional[str] = None
    ):
        self.__dict__.update(locals())
        del self.self