from bs4 import BeautifulSoup
import os
import requests
from common.chromedriver import Chromedriver
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


class Navermap():
    def __init__(self, channel_code, channel_name, url, keyword, logger, config, mongo) -> None:
        self.channel_code = channel_code
        self.channel_name   = channel_name
        self.keyword = keyword
        self.page = 1
        self.url = f'https://map.naver.com/p/api/search/allSearch?query={self.keyword}&type=all&searchCoord=126.88347%3B37.491377&page={self.page}'
        self.logger = logger
        # chromedriver = Chromedriver()
        # chromedriver.Decompress_Chrome_Driver()
        # chrome_path = f'{chromedriver.driver_path}/{chromedriver.current_version}/chromedriver-win32/chromedriver.exe'
        # self.driver = webdriver.Chrome(executable_path=chrome_path)
        self.config = config
        self.success_count = 0
        self.error_count = 0
        self.mongo = mongo

    def crawl_naver_map(self):
        try:
            res = requests.get(self.url)
            if res.status_code == 200:
                data = json.loads(res.text)
                place_list = data['result']['place']['list']
                for place in place_list:
                    try:
                        name = place['name']
                        phone = place['tel']
                        category = place['category']
                        address = place['address']
                        road_address = place['roadAddress']
                        thum_image = place['thumUrl']
                        lng = place['x']
                        lat = place['y']

                        self.mongo.InsertClimbInfo(name, phone, category, address, road_address, thum_image, lng, lat)
                    except Exception as e:
                        self.logger.error(f'[FAILED] crawl_naver_map  ::  {place}  >>  {e}')
        except Exception as e:
            self.logger.error(f'[FAILED] crawl_naver_map  >>  {e}')