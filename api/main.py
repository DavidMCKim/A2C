from app.router import mysql
import configparser
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
    

def create_app():
    app = FastAPI()

    app.include_router(mysql.router)

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
    # 개 불러오기
    config = configparser.ConfigParser()
    config.read('config.ini')
    main()