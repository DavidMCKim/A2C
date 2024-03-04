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
        ScrapChannels(server, channel_code, mongo)

    except Exception as e:
        logger.error(e)

def ScrapChannels(server, channel_code, mongo):
    try:
        channel_name=config['A2C_CHANNEL_CODE'][f'{channel_code}']
        logger.info(f'{now_date}_{channel_name} 수집시작')

        if channel_code == '3001':
            from channel.navermap import Navermap
            keyword_list = ['서울', '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
            url = 'https://www.map.naver.com'
            for keyword in keyword_list:
                try:
                    keyword += ' 클라이밍'
                    navermap = Navermap(channel_code, channel_name, url, keyword, logger, config, mongo)
                    navermap.crawl_naver_map()
                except Exception as e:
                    logger.error(f'[FAILED] {keyword} 수집 에러')
    except Exception as e:
        logger.error()
    

if __name__ == "__main__":
    ProcessChannel()