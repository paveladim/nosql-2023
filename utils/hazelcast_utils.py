# import hazelcast


# def get_hazelcast_client():
#     client = hazelcast.HazelcastClient()
#     return client


# hazelcast_client = get_hazelcast_client()


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


# def lock_reservation(reservation_id):
#     try:
#         reservation_lock = hazelcast_client.cp_subsystem.get_lock("myLock@group" +
#                                                              str(reservation_id)).blocking()
#         fence = reservation_lock.try_lock()
#         if fence != reservation_lock.INVALID_FENCE:
#             print(f"Ticket ID {reservation_id} locked successfully.")
#             return True
#         print(f"Ticket ID {reservation_id} is already locked.")
#         return False
#     except Exception as e:
#         print(f"Error locking ticket ID {reservation_id}: {e}")
#         return False


# def unlock_reservation(reservation_id):
#     try:
#         reservation_lock = hazelcast_client.cp_subsystem.get_lock("myLock@group" +
#                                                              str(reservation_id)).blocking()
#         reservation_lock.unlock()
#         print(f"Ticket ID {reservation_id} unlocked successfully.")
#     except Exception as e:
#         print(f"Error unlocking ticket ID {reservation_id}: {e}")