import uvicorn
import os
from fastapi import FastAPI
from utils.mongo_utils import connect_and_init_db, close_db_connect

app = FastAPI()


@app.get("/")
async def read_root():
    print(os.getenv('MONGO_URI'))
    return {"Hello" : "World"}

app.add_event_handler("startup", connect_and_init_db)
app.add_event_handler("shutdown", close_db_connect)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)