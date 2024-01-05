import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from utils.mongo_utils import connect_and_init_db, close_db_connect
from routers.apartments_router import apartments_router
from routers.clients_router import clients_router
from routers.reservations_router import reservations_router


app = FastAPI()
load_dotenv()

app.include_router(apartments_router, tags=["Apartment"], prefix="/apartments")
app.include_router(clients_router, tags=["Client"], prefix="/clients")
app.include_router(reservations_router, tags=["Reservation"], prefix="/reservations")

app.add_event_handler("startup", connect_and_init_db)
app.add_event_handler("shutdown", close_db_connect)


@app.get("/")
async def read_root():
    print(os.getenv('MONGO_URI'))
    return {"Hello" : "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)