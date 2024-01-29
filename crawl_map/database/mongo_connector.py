import requests
import json

class MONGO():
    def __init__(self) -> None:
        self.SOCIAL_API_SERVER_IP='http://127.0.0.1:10830/db'

    def GetServerInfo(self, hostname):
        try:
            url = self.SOCIAL_API_SERVER_IP + '/mongodb/GetServerInfo'

            data = {
                "hostname" : f'{hostname}'
            }
            
            req = requests.post(url, json=data, verify=False).text
            res = json.loads(req)

            channel_code = res['channel_code']
            status       = res['status']
            return channel_code, status
        
        except Exception as e:
            channel_code = '-2'
            server_os = '-2'
            return channel_code, server_os
        
        # InsertClimbInfo
    def InsertClimbInfo(self, hostname):
        try:
            url = self.SOCIAL_API_SERVER_IP + '/mongodb/InsertClimbInfo'

            data = {
                "hostname" : f'{hostname}'
            }
            
            req = requests.post(url, json=data, verify=False).text
            res = json.loads(req)

            channel_code = res['channel_code']
            return channel_code
        
        except Exception as e:
            channel_code = '-2'
            server_os = '-2'
            return channel_code, server_os