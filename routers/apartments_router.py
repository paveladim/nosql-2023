from bson import ObjectId
from typing import Any
from fastapi import APIRouter, Depends, status
from starlette.responses import Response
from models.apartment import Apartment
from repository.apartments_repository import ApartmentRepository

apartments_router = APIRouter()


@apartments_router.get("/all")
async def get_all_apartments(repository: ApartmentRepository = Depends(ApartmentRepository.get_apartment_repo_instance)) -> list[Apartment]:
    return await repository.get_all()


@apartments_router.get("/{apartment_id}", response_model=Apartment)
async def get_apartment_by_id(apartment_id: str, repository: ApartmentRepository = Depends(ApartmentRepository.get_apartment_repo_instance)) -> Any:
    if not ObjectId.is_valid(apartment_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    
    apartment = await repository.get_by_id(apartment_id)

    if apartment is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    return apartment