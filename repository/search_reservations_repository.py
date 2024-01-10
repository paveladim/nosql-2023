import os

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from datetime import datetime

from utils.elasticsearch_utils import get_elasticsearch_client
from models.reservation import Reservation, UpdateReservationModel


class SearchReservationsRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    def __init__(self, index: str, elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_client = elasticsearch_client
        self._elasticsearch_index = index

    async def create(self, reservation_id: str, reservation: UpdateReservationModel):
        await self._elasticsearch_client.create(index=self._elasticsearch_index, id=reservation_id, document=dict(reservation))

    async def update(self, reservation_id: str, reservation: UpdateReservationModel):
        await self._elasticsearch_client.update(index=self._elasticsearch_index, id=reservation_id, doc=dict(reservation))

    async def delete(self, reservation_id: str):
        await self._elasticsearch_client.delete(index=self._elasticsearch_index, id=reservation_id)

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
        reservations = list(map(lambda reservation: Reservation(
            id=reservation['_id'], 
            client_id=reservation['_source']['client_id'],
            apartment_id=reservation['_source']['apartment_id'],
            start_date=datetime(reservation['_source']['start_date']),
            end_date=datetime(reservation['_source']['end_date']),
            status=reservation['_source']['status']), result))
        return reservations

    @staticmethod
    def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = os.getenv('ELASTICSEARCH_RESERVATION_INDEX')
        return SearchReservationsRepository(elasticsearch_index, elasticsearch_client)