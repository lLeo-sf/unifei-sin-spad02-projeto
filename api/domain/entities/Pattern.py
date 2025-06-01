from api.domain.entities.BaseEntity import BaseEntity

class Pattern(BaseEntity):
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
