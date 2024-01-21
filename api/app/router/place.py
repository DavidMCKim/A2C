import configparser
from http import server
from fastapi import APIRouter, Request
from app.database.mongo_connector import MONGO

config = configparser.ConfigParser()
config.read('config.ini')

db = MONGO()

router = APIRouter(prefix='/db/mongo')

@router.post('/InsertClimbInfo')
async def get_server_info(request: Request):
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

@router.post('/RecommandRecentPlace')
async def get_server_info(request: Request):
    server_info = {
        'address_main'    : '-1',
        'address_detail'  : '-1',
        'place_name'      : '-1',
        'star_score'      : '-1',
        'keyword'         : '-1'
    }
    try:
        startdate = request['startdate']
        enddate = request['enddate']
        req = await request.json()
        hostname = req['hostname']
        query = f'''
                    select Address_main, Address_detail, Place_Name, Star_Scroe, Keyword
                    from Map_Naver_Place
                    where RegDate between '{startdate}' and '{enddate}'
                    order by RegDate desc
                '''
        data = db.select(query)
        if data:
            server_info = {
                'address_main'    : f'{data[0]}',
                'address_detail'  : f'{data[1]}',
                'place_name'      : f'{data[2]}',
                'star_score'      : f'{float(data[3])}',
                'keyword'         : f'{data[4]}'
            }
    except Exception as e:
        print(e)

    return server_info