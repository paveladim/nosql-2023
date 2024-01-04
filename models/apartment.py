from pydantic import BaseModel


class Apartment(BaseModel):
    id: str
    state: str
    address: str


class UpdateApartmentModel(BaseModel):
    state: str
    address: str