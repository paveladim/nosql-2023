from fastapi import APIRouter, Depends
from models.client import Client
from repository.clients_repository import ClientRepository

clients_router = APIRouter()

@clients_router.get("/all")
async def get_all_clients(repository: ClientRepository = Depends(ClientRepository.get_client_repo_instance)) -> list[Client]:
    return await repository.get_all()