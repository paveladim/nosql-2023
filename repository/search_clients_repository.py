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

    async def find_by_name(self, name: str):
        index_exist = await self._elasticsearch_client.indices.exists(index=self._elasticsearch_index)

        if not index_exist:
            return []

        query = {
            "match": {
                "name": {
                    "query": name
                }
            }
        }
        response = await self._elasticsearch_client.search(index=self._elasticsearch_index, query=query, filter_path=['hits.hits._id', 'hits.hits._source'])
        if 'hits' not in response.body:
            return []
        result = response.body['hits']['hits']
        clients = list(map(lambda client: Client(
            id=client['_id'], 
            name=client['_source']['name'], 
            surname=client['_source']['surname'], 
            age=int(client['_source']['age']),
            phone=client['_source']['phone'],
            email=client['_source']['email']), result))
        return clients

    @staticmethod
    def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = os.getenv('ELASTICSEARCH_CLIENT_INDEX')
        return SearchClientsRepository(elasticsearch_index, elasticsearch_client)