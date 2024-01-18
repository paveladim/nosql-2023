import os

from elasticsearch import AsyncElasticsearch

elasticsearch_client: AsyncElasticsearch = None


def get_elasticsearch_client() -> AsyncElasticsearch:
    return elasticsearch_client


async def connect_and_init_elasticsearch():
    global elasticsearch_client
    elasticsearch_uri = os.getenv('ELASTICSEARCH_URI')
    try:
        elasticsearch_client = AsyncElasticsearch(elasticsearch_uri.split(','))
        await elasticsearch_client.info()
        print(f'Connected to elasticsearch with uri {elasticsearch_uri}')
    except Exception as e:
        print(f'Cant connect to elasticsearch: {e}')


async def close_elasticsearch_connect():
    global elasticsearch_client
    if elasticsearch_client is None:
        return
    await elasticsearch_client.close()


async def create_client_index():
    try:
        mappings = {
            "properties": {
                "name": {"type": "text"},
                "surname": {"type": "text"},
                "age": {"type": "int"},
                "phone": {"type": "text"},
                "email": {"type": "text"}
            }
        }
 
        es_client = get_elasticsearch_client()
        response = await es_client.indices.create(index=os.getenv('ELASTICSEARCH_CLIENT_INDEX'), mappings=mappings)
        return response
    except Exception as e:
        print(f"Error creating client index: {e}")
        return None
    
 
async def create_apartment_index():
    try:
        mappings = {
            "properties": {
                "state": {"type": "text"},
                "address": {"type": "text"},
                "zipcode": {"type": "int"},
                "bedrooms" : {"type": "int"},
                "bathroom": {"type": "text"},
                "wifi": {"type": "text"},
                "kitchen": {"type": "text"}
            }
        }
 
        es_client = get_elasticsearch_client()
        response = await es_client.indices.create(index=os.getenv('ELASTICSEARCH_APARTMENT_INDEX'), mappings=mappings)
        return response
    except Exception as e:
        print(f"Error creating apartment index: {e}")
        return None
 
 
async def create_reservation_index():
    try:
        mappings = {
            "properties": {
                "client_id": {"type": "text"},
                "apartment_id": {"type": "text"},
                "start_date": {"type": "text"},
                "end_date": {"type": "text"},
                "status": {"type": "text"}
            }
        }
 
        es_client = get_elasticsearch_client()
        response = await es_client.indices.create(index=os.getenv('ELASTICSEARCH_RESERVATION_INDEX'), mappings=mappings)
        return response
    except Exception as e:
        print(f"Error creating reservation index: {e}")
        return None