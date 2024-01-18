from bson import ObjectId
from typing import Any
from fastapi import APIRouter, Depends, status, HTTPException
from starlette.responses import Response
from pymemcache import HashClient
from datetime import date, datetime, timedelta

from models.reservation import Reservation, UpdateReservationModel
from repository.reservations_repository import ReservationRepository
from repository.search_reservations_repository import SearchReservationsRepository
from utils.hazelcast_utils import lock_apartment, unlock_apartment
from cache.memcached_utils import get_memcached_client
from utils.mongo_utils import date_format, map_update_reservation, map_reservation

reservations_router = APIRouter()


@reservations_router.get("/all")
async def get_all_reservations(repository: ReservationRepository = Depends(ReservationRepository.get_reservation_repo_instance)):
    return await repository.get_all()


@reservations_router.post("/{client_id}/book/{apartment_id}/{year}/{month}/{day}/{count}")
async def book_apartment(client_id: str, apartment_id: str, year: int, month: int, day: int, count: int,
                         rs_repo: ReservationRepository = Depends(ReservationRepository.get_reservation_repo_instance),
                         srs_repo: SearchReservationsRepository = Depends(SearchReservationsRepository.get_instance)):
    #reservations = await srs_repo.find_by_apartment_id(apartment_id)
    reservations = await rs_repo.get_all_by_apartment_id(apartment_id)
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
        #if not lock_apartment(apartment_id):
        #    raise HTTPException(status_code=400, detail="Cannot block apartment")
        
        own_r = map_update_reservation({
            'client_id' : client_id,
            'apartment_id' : apartment_id,
            'start_date' : st.strftime('%Y-%m-%d'),
            'end_date' : ed.strftime('%Y-%m-%d'),
            'status' : 'Booked'
        })

        own_id = await rs_repo.create(own_r)
        #unlock_apartment(apartment_id)
        return map_reservation({'_id' : own_id,
                                'client_id' : client_id,
                                'apartment_id' : apartment_id,
                                'start_date' : st.strftime('%Y-%m-%d'),
                                'end_date' : ed.strftime('%Y-%m-%d'),
                                'status' : 'Booked'})
    
    else:
        raise HTTPException(status_code=400, detail="This apartment was booked or bought for your dates")


@reservations_router.put("/pay/{reservation_id}")
async def pay_apartment(reservation_id: str,
                         rs_repo: ReservationRepository = Depends(ReservationRepository.get_reservation_repo_instance),
                         srs_repo: SearchReservationsRepository = Depends(SearchReservationsRepository.get_instance)):
    if not ObjectId.is_valid(reservation_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    reservation = await rs_repo.get_by_id(reservation_id)

    if reservation.status != 'Booked':
        raise HTTPException(status_code=400, detail="This apartment was not booked")

    payment_successful = True
    if payment_successful:
        reservation.status = 'Paid'

        reservation = await rs_repo.update(reservation_id, reservation)
        if reservation is None:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        return {'Payment' : 'Success'}
    else:
        return {'Payment' : 'Failed'}

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