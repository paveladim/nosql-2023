import hazelcast


def get_hazelcast_client():
    client = hazelcast.HazelcastClient()
    print('Hazelcast')
    return client


hazelcast_client = None


def get_hazelcast_client():
    return hazelcast_client


def connect_and_init_hazelcast():
    global hazelcast_client
    try:
        hazelcast_client = hazelcast.HazelcastClient(cluster_members=["localhost:5701"])
        print(f'Connected to hazelcast')
    except Exception as e:
        print(f'Cant connect to memcached: {e}')


def close_hazelcast_connect():
    global hazelcast_client
    if hazelcast_client is None:
        return
    hazelcast_client.shutdown()


# def cache_reservation(reservation_id, reservation):
#     try:
#         stations_map = hazelcast_client.get_map("reservations")
#         future_station_data = stations_map.put(reservation_id, reservation)
#         result = future_station_data.result()
#         print(f"Station data cached for station ID: {reservation_id}")
#         return result
#     except Exception as e:
#         print(f"Error caching station data for station ID {reservation_id}: {e}")
#         return None


# async def get_cached_reservation(reservation_id):
#     try:
#         reservations_map = hazelcast_client.get_map("reservations")
#         future_reservation_data = reservations_map.get(reservation_id)
#         reservation_data = future_reservation_data.result()

#         if reservation_data is None:
#             print(f"No data found in cache for station ID: {reservation_id}")
#             return None

#         print(f"Retrieved data from cache for station ID: {reservation_id}")
#         return reservation_data
#     except Exception as e:
#         print(f"Error retrieving station data for station ID {reservation_id}: {e}")
#         return e


def lock_apartment(apartment_id):
    try:
        hazelcast_client = get_hazelcast_client()
        apartment_lock = hazelcast_client.cp_subsystem.get_lock("myLock@group" +
                                                             str(apartment_id)).blocking()
        fence = apartment_lock.try_lock()
        if fence != apartment_lock.INVALID_FENCE:
            print(f"Apartment ID {apartment_id} locked successfully.")
            return True
        print(f"Apartment ID {apartment_id} is already locked.")
        return False
    except Exception as e:
        print(f"Error locking apartment ID {apartment_id}: {e}")
        return False


def unlock_apartment(apartment_id):
   try:
       hazelcast_client = get_hazelcast_client()
       apartment_lock = hazelcast_client.cp_subsystem.get_lock("myLock@group" +
                                                             str(apartment_id)).blocking()
       apartment_lock.unlock()
       print(f"Apartment ID {apartment_id} unlocked successfully.")
   except Exception as e:
       print(f"Error unlocking apartment ID {apartment_id}: {e}")