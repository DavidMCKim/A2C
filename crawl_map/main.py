from csv import excel_tab
import os, copy
import sys
import linecache
import string
import smtplib
import json
import requests
import logging
import urllib
from database.mongo_connector import MONGO
from datetime import datetime
from loguru import logger
import socket
import configparser
# from dotenv import load_dotenv

# # load .env
# load_dotenv()
## .env파일에서 서버 정보 가져오기
# server = os.environ.get('APP_CONFIG')

config = configparser.ConfigParser()
config.read('common/config.ini')

# 프로그램 시작 시 현재 날짜 조회하기
now = datetime.now()
now_date = datetime.strftime(now,'%Y-%m-%d')

# 프로그램 폴더 내 log폴더 안에 날짜와 라운드별 로그파일 설정하기
logger.add(f"./log/{now_date}_", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}") 

def ProcessChannel():
    try:
        # DB클래스 호출
        mongo = MONGO()
        
        # 현재 프로그램 실행중인 hostname 조회하기
        hostname = socket.gethostname()

        channel_code, server = mongo.GetServerInfo(hostname)
        # 채널별 수집
        ScrapChannels(server, channel_code)

    except Exception as e:
        logger.error(e)

def ScrapChannels(server, channel_code):
    try:
        channel_name=config['DMP_CHANNELS'][f'{channel_code}']
        logger.info(f'{now_date}_{channel_name} 수집시작')

        if channel_code == 3001:
            from channel.navermap import Navermap
            navermap = Navermap()

        # if channel_code == 3000:
        #     from channel.coupang import Coupang
        #     # coupang = Coupang(server, channel_code, channel_name, placement, url)

        # elif channel_code == 3004:
        #     from channel.auction import Auction
        #     # elevenst = Auction(server, channel_code, channel_name, placement, url)

        # elif channel_code == 3005:
        #     from channel.gmarket import Gmarket
        #     # elevenst = Gmarket(server, channel_code, channel_name, placement, url)
    except Exception as e:
        logger.error()
    

if __name__ == "__main__":
    ProcessChannel()