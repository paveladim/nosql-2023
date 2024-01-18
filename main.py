import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from handler.event_handlers import startup, shutdown
from routers.apartments_router import apartments_router
from routers.clients_router import clients_router
from routers.reservations_router import reservations_router
from utils.elasticsearch_utils import create_client_index, create_apartment_index, create_reservation_index
 
 
app = FastAPI()
load_dotenv()
 
app.include_router(apartments_router, tags=["Apartment"], prefix="/apartments")
app.include_router(clients_router, tags=["Client"], prefix="/clients")
app.include_router(reservations_router, tags=["Reservation"], prefix="/reservations")
 
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)
 
 
@app.get("/")
async def read_root():
    print(os.getenv('MONGO_URI'))
    return {"Hello" : "World"}
 
 
@app.get("/create_client_indices")
async def create_ci():
    await create_client_index()
    return {"Client" : "Indices"}
 
 
@app.get("/create_apartment_indices")
async def create_ai():
    await create_apartment_index()
    return {"Apartment" : "Indices"}
 
 
@app.get("/create_reservation_indices")
async def create_ri():
    await create_reservation_index()
    return {"Reservation" : "Indices"}
 
 
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)