import configparser
from http import server
from fastapi import APIRouter, Request
from app.database.mongo_connector import MONGO

config = configparser.ConfigParser()
config.read('config.ini')

db = MONGO()

router = APIRouter(prefix='/db/mongo')

@router.post('/InsertClimbInfo')
async def insert_climb_info(request: Request):
    server_info = {
        'channel_code' : '-1'
    }
    try:
        req = await request.json()
        hostname = req['hostname']
        query = f'''
                    select ChannelCode
                    from tb_Server_Info
                    where ServerName = '{hostname}'
                '''
        data = db.select(query)
        if data:
            channel_cdoe = data[0]

            server_info = {
                'channel_code' : f'{channel_cdoe}'
            }
    except Exception as e:
        print(e)

    return server_info