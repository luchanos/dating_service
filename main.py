from datetime import datetime
from typing import Optional

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from pydantic import BaseModel
from starlette.requests import Request
from elasticsearch import AsyncElasticsearch

MAPPING_FOR_INDEX = {
    "mappings":
        {
            "properties": {
                "name": {
                    "type": "text"
                },
                "surname": {
                    "type": "text"
                },
                "date_of_birth": {
                    "type": "date"
                },
                "interests": {
                    "type": "text"
                }
            }
        }
}


async def ping() -> dict:
    return {"Success": True}


async def create_index(request: Request) -> dict:
    elastic_client = request.app.state.elastic_client
    await elastic_client.indices.create(index="users", body=MAPPING_FOR_INDEX)
    return {"Success": True}


async def delete_index(request: Request) -> dict:
    elastic_client = request.app.state.elastic_client
    await elastic_client.indices.delete(index="users")
    return {"Success": True}


class CreateUserRequest(BaseModel):
    name: str
    surname: Optional[str]
    date_of_birth: Optional[datetime]
    interests: Optional[list[str]]


async def create_user(request: Request, body: CreateUserRequest) -> dict:
    elastic_client = request.app.state.elastic_client
    await elastic_client.index(index="users", document=body.dict())
    return {"Success": True}


routes = [
    APIRoute(path="/ping", endpoint=ping, methods=["GET"]),
    APIRoute(path="/create_index", endpoint=create_index, methods=["GET"]),
    APIRoute(path="/delete_index", endpoint=delete_index, methods=["GET"]),
    APIRoute(path="/create_user", endpoint=create_user, methods=["POST"]),
]

elastic_client = AsyncElasticsearch()
app = FastAPI()
app.state.elastic_client = elastic_client
app.include_router(APIRouter(routes=routes))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)