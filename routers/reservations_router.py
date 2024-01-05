from fastapi import APIRouter, Depends
from models.reservation import Reservation, UpdateReservationModel
from repository.reservations_repository import ReservationRepository

reservations_router = APIRouter()


@reservations_router.post("/")
async def add_reservation(reservation: UpdateReservationModel,
                      repository: ReservationRepository = Depends(ReservationRepository.get_reservation_repo_instance)) -> str:
    reservation_id = await repository.create(reservation)
    #await search_repository.create(reservation_id, reservation)
    return reservation_id