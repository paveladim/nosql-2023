from datetime import datetime
from pydantic import BaseModel


class Reservation(BaseModel):
    id: str
    client_id: str
    apartment_id: str
    start_date: datetime
    end_date: datetime
    status: str

class UpdateReservationModel(BaseModel):
    client_id: str
    apartment_id: str
    start_date: datetime
    end_date: datetime
    status: str