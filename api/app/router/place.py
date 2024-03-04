import configparser
from http import server
from fastapi import APIRouter, Request
from app.database.mongo_connector import MONGO

db = MONGO()

router = APIRouter(prefix='/db/mongodb')

@router.post('/GetServerInfo')
async def GetServerInfo(request: Request):
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
async def InsertClimbInfo(request: Request):
    server_info = {
        'channel_code' : '-1'
    }
    try:
        req = await request.json()
        name = req['name']
        phone = req['phone']
        address = req['address']
        road_address = req['road_address']
        thum_image = req['thum_image']
        lng = req['lng']
        lat = req['lat']
        collection = 'tb_place_of_climbing'
        data = {
                "PlaceName" : f'{name}',
                'Tel': f'{phone}',
                'Address':f'{address}',
                'RoadAddress':f'{road_address}',
                'ImgUrl':f'{thum_image}',
                'Lng':f'{lng}',
                'Lat':f'{lat}',
            }
        result = db.insert_one(collection, data)
        if data:
            channel_cdoe = data[0]

            server_info = {
                'channel_code' : f'{channel_cdoe}'
            }
    except Exception as e:
        print(e)

    return server_info