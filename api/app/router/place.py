import configparser
from http import server
from fastapi import APIRouter, Request
from app.database.mongo_connector import MONGO

db = MONGO()

router = APIRouter(prefix='/db/mongodb')

@router.post('/GetServerInfo')
async def insert_climb_info(request: Request):
    server_info = {
        'channel_code' : '-1',
        'status'       : '-1'
    }
    try:
        req = await request.json()
        hostname = req['hostname']
        collection = 'tb_server_info'
        data = {'ServerName':f'{hostname}'}
        result = db.select(collection, data)
        if result:
            channel_code = result['ChannelCode']
            status = result['Status']
            server_info = {
                'channel_code' : f'{channel_code}',
                'status'       : f'{status}'
            }
    except Exception as e:
        print(e)

    return server_info

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