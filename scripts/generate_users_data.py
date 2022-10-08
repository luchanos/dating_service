import asyncio

from elasticsearch import AsyncElasticsearch, RequestError

from main import MAPPING_FOR_INDEX

user_1 = {
  "name": "Ivan",
  "surname": "Petrov",
  "date_of_birth": "1996-01-01",
  "interests": ["programming", "mma"]
}

user_2 = {
  "name": "Anna",
  "surname": "Lavrova",
  "date_of_birth": "1997-02-03",
  "interests": ["dancing", "singing"]
}

user_3 = {
    "name": "Petr"
}

user_4 = {
  "name": "Sergey",
  "date_of_birth": "1986-06-01"
}

user_5 = {
  "name": "Kseniia",
  "date_of_birth": "2000-10-10",
  "interests": ["programming", ]
}

user_list = [user_1, user_2, user_3, user_4, user_5]


async def main():
    elastic_client = AsyncElasticsearch()
    try:
        await elastic_client.indices.create(index="users", mappings=MAPPING_FOR_INDEX)
    except RequestError as err:
        print(err)
    for document in user_list:
        await elastic_client.index(index="users", document=document)


asyncio.run(main())
