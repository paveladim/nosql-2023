import os

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from utils.elasticsearch_utils import get_elasticsearch_client
from models.apartment import Apartment, UpdateApartmentModel


class SearchApartmentsRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    def __init__(self, index: str, elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_client = elasticsearch_client
        self._elasticsearch_index = index

    async def create(self, client_id: str, client: UpdateApartmentModel):
        await self._elasticsearch_client.create(index=self._elasticsearch_index, id=client_id, document=dict(client))

    async def update(self, client_id: str, client: UpdateApartmentModel):
        await self._elasticsearch_client.update(index=self._elasticsearch_index, id=client_id, doc=dict(client))

    async def delete(self, client_id: str):
        await self._elasticsearch_client.delete(index=self._elasticsearch_index, id=client_id)

    async def find_by_state(self, state: str):
        print(state)
        index_exist = await self._elasticsearch_client.indices.exists(index='apartments')

        if not index_exist:
            return []

        query = {
            "match": {
                "state": {
                    "query": state
                }
            }
        }
        response = await self._elasticsearch_client.search(index=self._elasticsearch_index, query=query, filter_path=['hits.hits._id', 'hits.hits._source'])
        if 'hits' not in response.body:
            return []
        result = response.body['hits']['hits']
        apartments = list(map(lambda apartment: Apartment(
            id=apartment['_id'],
            state=apartment['_source']['state'],
            address=apartment['_source']['address'],
            zipcode=apartment['_source']['zipcode'],
            bedrooms=int(apartment['_source']['bedrooms']),
            bathroom=apartment['_source']['bathroom'],
            wifi=apartment['_source']['wifi'],
            kitchen=apartment['_source']['kitchen']), result))
        return apartments

    @staticmethod
    def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = os.getenv('ELASTICSEARCH_APARTMENT_INDEX')
        return SearchApartmentsRepository(elasticsearch_index, elasticsearch_client)