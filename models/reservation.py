from pydantic import BaseModel


class Reservation(BaseModel):
    id: str
    client_id: int
    apartment_id: int
    start_date: Datetime
    end_date: Datetime
    status: str

class UpdateReservationModel(BaseModel):
    client_id: int
    apartment_id: int
    start_date: Datetime
    end_date: Datetime
    status: str