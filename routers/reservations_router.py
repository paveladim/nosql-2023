from bson import ObjectId
from typing import Any
from fastapi import APIRouter, Depends, status
from starlette.responses import Response
from pymemcache import HashClient

from models.reservation import Reservation, UpdateReservationModel
from repository.reservations_repository import ReservationRepository
from cache.memcached_utils import get_memcached_client

reservations_router = APIRouter()


@reservations_router.post("/")
async def add_reservation(reservation: UpdateReservationModel,
                      repository: ReservationRepository = Depends(ReservationRepository.get_reservation_repo_instance)) -> str:
    reservation_id = await repository.create(reservation)
    #await search_repository.create(reservation_id, reservation)
    return reservation_id