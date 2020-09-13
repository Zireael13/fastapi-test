# app.py
import uvicorn
from fastapi import FastAPI
from typing import Optional
from elasticsearch import AsyncElasticsearch



app = FastAPI()
es = AsyncElasticsearch()


#hello word example
@app.get('/')
def home():
    return {'hello': 'world'}

#demo endpoint
@app.get('/analytics')
def analytics(url: str):
    print(url)
    return {'url': url}


@app.on_event("shutdown")
async def app_shutdown():
    #closes elasticsearch connection
    await es.close()


if __name__ == '__main__':
    uvicorn.run(app)