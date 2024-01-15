import json
from bson import ObjectId
from typing import Any
from fastapi import APIRouter, Depends, status
from starlette.responses import Response
from pymemcache import HashClient

from models.client import Client, UpdateClientModel
from repository.clients_repository import ClientRepository
from repository.search_clients_repository import SearchClientsRepository
from cache.memcached_utils import get_memcached_client

clients_router = APIRouter()


@clients_router.get("/all")
async def get_all_clients(repository: ClientRepository = Depends(ClientRepository.get_client_repo_instance)) -> list[Client]:
    return await repository.get_all()


@clients_router.get("/{client_id}", response_model=Client)
async def get_clients_by_id(client_id: str, 
                            repository: ClientRepository = Depends(ClientRepository.get_client_repo_instance),
                            memcached_client: HashClient = Depends(get_memcached_client)) -> Any:
    if not ObjectId.is_valid(client_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    
    client = memcached_client.get(client_id)

    if client is not None:
        return client
    
    client = await repository.get_by_id(client_id)

    if client is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    return client

@clients_router.post("/srv/post_all")
async def fill_clients(repository: ClientRepository = Depends(ClientRepository.get_client_repo_instance),
                       search_repo: SearchClientsRepository = Depends(SearchClientsRepository.get_instance)):
    with open('./clients_.json', 'r') as src:
        clients_list = json.load(src)
        for cl in clients_list:
            client = UpdateClientModel(
                name=cl['name'], 
                surname=cl['surname'],
                age=int(cl['age']),
                phone=cl['phone_number'],
                email=cl['email'])
            current_id = await repository.create(client)
            search_repo.create(current_id, client=client)
