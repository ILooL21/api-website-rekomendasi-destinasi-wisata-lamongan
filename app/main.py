from fastapi import FastAPI
from app.db.session import check_db_connection

app = FastAPI()

# check database connection
check_db_connection()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
