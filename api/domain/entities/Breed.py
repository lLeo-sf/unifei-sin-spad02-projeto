from api.domain.entities.BaseEntity import BaseEntity


class Breed(BaseEntity):
    def __init__(self, name: str):
        self.name = name
