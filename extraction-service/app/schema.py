from typing import Literal
from pydantic import BaseModel, Field, ConfigDict, model_validator

class Room(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    id: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=100)
    type: Literal['bedroom','bathroom','kitchen','living','hall','other']
    area: float | None = Field(ge=0, le=100000)

class Layout(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    unit: Literal['sqft','sqm']
    area_basis: Literal['internal','gross','unknown']
    total_area: float | None = Field(gt=0, le=1000000)
    bedrooms: int | None = Field(ge=0, le=100)
    bathrooms: float | None = Field(ge=0, le=100, multiple_of=.5)
    doors: int | None = Field(ge=0, le=1000)
    windows: int | None = Field(ge=0, le=1000)
    rooms: list[Room] = Field(max_length=200)
    warnings: list[str] = Field(max_length=50)

    @model_validator(mode='after')
    def unique_rooms(self):
        if len({r.id for r in self.rooms}) != len(self.rooms):
            raise ValueError('Duplicate room IDs')
        return self
