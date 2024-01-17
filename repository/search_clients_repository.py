import os

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from utils.elasticsearch_utils import get_elasticsearch_client
from models.client import Client, UpdateClientModel


class SearchClientsRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str


    def __init__(self, index: str, elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_client = elasticsearch_client
        self._elasticsearch_index = index


    async def create(self, client_id: str, client: UpdateClientModel):
        await self._elasticsearch_client.create(index=self._elasticsearch_index, id=client_id, document=dict(client))


    async def update(self, client_id: str, client: UpdateClientModel):
        await self._elasticsearch_client.update(index=self._elasticsearch_index, id=client_id, doc=dict(client))


    async def delete(self, client_id: str):
        await self._elasticsearch_client.delete(index=self._elasticsearch_index, id=client_id)


    @staticmethod
    def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = os.getenv('ELASTICSEARCH_CLIENT_INDEX')
        return SearchClientsRepository(elasticsearch_index, elasticsearch_client)