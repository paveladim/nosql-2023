import hazelcast


def get_hazelcast_client():
    client = hazelcast.HazelcastClient()
    return client


hazelcast_client = get_hazelcast_client()


def cache_station(station_id, station_data):
    try:
        stations_map = hazelcast_client.get_map("stations")
        future_station_data = stations_map.put(station_id, station_data)
        result = future_station_data.result()
        print(f"Station data cached for station ID: {station_id}")
        return result
    except Exception as e:
        print(f"Error caching station data for station ID {station_id}: {e}")
        return None


async def get_cached_station(station_id):
    try:
        stations_map = hazelcast_client.get_map("stations")
        future_station_data = stations_map.get(station_id)
        station_data = future_station_data.result()

        if station_data is None:
            print(f"No data found in cache for station ID: {station_id}")
            return None

        print(f"Retrieved data from cache for station ID: {station_id}")
        return station_data
    except Exception as e:
        print(f"Error retrieving station data for station ID {station_id}: {e}")
        return e


def lock_ticket(ticket_id):
    try:
        ticket_lock = hazelcast_client.cp_subsystem.get_lock("myLock@group" +
                                                             str(ticket_id)).blocking()
        fence = ticket_lock.try_lock()
        if fence != ticket_lock.INVALID_FENCE:
            print(f"Ticket ID {ticket_id} locked successfully.")
            return True
        print(f"Ticket ID {ticket_id} is already locked.")
        return False
    except Exception as e:
        print(f"Error locking ticket ID {ticket_id}: {e}")
        return False


def unlock_ticket(ticket_id):
    try:
        ticket_lock = hazelcast_client.cp_subsystem.get_lock("myLock@group" +
                                                             str(ticket_id)).blocking()
        ticket_lock.unlock()
        print(f"Ticket ID {ticket_id} unlocked successfully.")
    except Exception as e:
        print(f"Error unlocking ticket ID {ticket_id}: {e}")