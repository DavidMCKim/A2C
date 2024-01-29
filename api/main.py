from app.router import place
import configparser
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

def create_app():
    app = FastAPI()
    app.include_router(place.router)
    return app

app = create_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=[]
)

def main():
    uvicorn.run(
        app="main:app",
        host=config['APP']['host'],
        port=int(config['APP']['port']),
        reload=True
    )
    
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(f'app/common/config.ini')
    main()