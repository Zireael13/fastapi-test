# app.py
import uvicorn
from fastapi import FastAPI
import asyncio
import requests

# from typing import Optional
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from pydantic import BaseSettings


class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_HOST: str = (
        "search-matt-test-wzk7emgc5uns46u42e5rygpoeq.us-east-2.es.amazonaws.com"
    )
    AWS_REGION: str = "us-east-2"

    class Config:
        env_file = ".env"
        env_prefix = ""
        allow_mutation = False
        case_senstive: True


settings = Settings()

service = "es"

awsauth = AWS4Auth(
    settings.AWS_ACCESS_KEY_ID,
    settings.AWS_SECRET_ACCESS_KEY,
    settings.AWS_REGION,
    service,
)

es = Elasticsearch(
    hosts=[{"host": settings.AWS_HOST, "port": 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)


app = FastAPI()


# hello word example
@app.get("/")
def home():
    print(asyncio)
    return {"hello": "world"}


@app.get("/ping")
def ping():
    ping = es.ping()

    print(f"ping: {ping}")
    return {"ping": ping}


# demo endpoint
@app.get("/analytics")
def analytics(url: str):
    query_body = {"query": {"match": {"text": {"query": url, "fuzziness": "AUTO"}}}}

    tweets = es.search(index="", body=query_body)
    print(tweets)
    print(url)
    return {"url": url}


@app.on_event("shutdown")
def app_shutdown():
    # closes elasticsearch connection
    es.close()


if __name__ == "__main__":
    uvicorn.run(app)