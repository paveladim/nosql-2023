from pydantic import BaseModel


class Apartment(BaseModel):
    id: str
    state: str
    address: str
    zipcode: int
    bedrooms: int
    bathroom_available: bool
    wifi_available: bool
    kitchen_available: bool
    bathroom_accessories_available: bool


class UpdateApartmentModel(BaseModel):
    state: str
    address: str
    zipcode: int
    bedrooms: int
    bathroom_available: bool
    wifi_available: bool
    kitchen_available: bool
    bathroom_accessories_available: bool