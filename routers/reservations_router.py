from bson import ObjectId
from typing import Any
from fastapi import APIRouter, Depends, status, HTTPException
from starlette.responses import Response
from pymemcache import HashClient
from datetime import date, datetime, timedelta

from models.reservation import Reservation, UpdateReservationModel
from repository.reservations_repository import ReservationRepository
from repository.search_reservations_repository import SearchReservationsRepository
#from utils.hazelcast_utils import lock_reservation, unlock_reservation
from cache.memcached_utils import get_memcached_client
from utils.mongo_utils import date_format

reservations_router = APIRouter()


@reservations_router.get("/all")
async def get_all_reservations(repository: ReservationRepository = Depends(ReservationRepository.get_reservation_repo_instance)):
    return await repository.get_all()


@reservations_router.post("/{client_id}/book/{apartment_id}/{year}/{month}/{day}/{count}")
async def book_apartment(client_id: str, apartment_id: str, year: int, month: int, day: int, count: int,
                         rs_repo: ReservationRepository = Depends(ReservationRepository.get_reservation_repo_instance),
                         srs_repo: SearchReservationsRepository = Depends(SearchReservationsRepository.get_instance)):
    reservations = await srs_repo.find_by_apartment_id(apartment_id)
    st = date(year, month, day)
    ed = st + timedelta(days=count)
    free = True
    for r in reservations:
        s = datetime.strptime(r.start_date, date_format).date()
        e = datetime.strptime(r.end_date, date_format).date()

        if s <= st <= e or s <= ed <= e:
            free = False

    if free:
        print("Apartment is free")
    else:
        raise HTTPException(status_code=400, detail="This apartment was booked or bought for your dates")


@reservations_router.post("/")
async def add_reservation(reservation: UpdateReservationModel,
                          repository: ReservationRepository = Depends(ReservationRepository.get_reservation_repo_instance),
                          search_repo: SearchReservationsRepository = Depends(SearchReservationsRepository.get_instance)) -> str:
    reservation_id = await repository.create(reservation)
    await search_repo.create(reservation_id, reservation)
    return reservation_id


@reservations_router.delete("/srv/delete_all")
async def remove_all(repository: ReservationRepository = Depends(ReservationRepository.get_reservation_repo_instance),
                     search_repo: SearchReservationsRepository = Depends(SearchReservationsRepository.get_instance)) -> Response:
    await repository.delete_all()
    return Response()