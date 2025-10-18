import requests

url='http://222.201.54.55/eportal/InterFace.do?method=login'
headers={
    'cookie':'EPORTAL_COOKIE_SERVER=; EPORTAL_COOKIE_DOMAIN=; EPORTAL_COOKIE_SAVEPASSWORD=true; EPORTAL_COOKIE_OPERATORPWD=; EPORTAL_COOKIE_USERNAME=32406500046; EPORTAL_COOKIE_NEWV=true; EPORTAL_COOKIE_PASSWORD=80d465bb3f55ad6d8f744e64b92303344ee60b73fb4ccdbdb0f594a8e4853875179d6ea8860d7edfe828691f2dd42985c7a1ef4ead1604b0125d680395c83103d8d2782474d752cbf5926012a050c2e589a08f40b3d7beef4a9d4fc02faa768baaade5684e357a3cf5aa9e9eb2a98d16d84ea034a086eb3005e554101d4ab73d; EPORTAL_AUTO_LAND=true; EPORTAL_USER_GROUP=4-24; EPORTAL_COOKIE_SERVER_NAME=; JSESSIONID=943D8FB76F9511D0F42D73AE1B3DD5F0',
    'host':'222.201.54.55',
    'origin':'http://222.201.54.55',
    'referer':'http://222.201.54.55/eportal/index.jsp?wlanuserip=172.26.201.76&wlanacname=AC&ssid=GZHU%2Dstudent&mac=A4-42-CD-72-8F-B7&url=http://123.123.123.123/',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
}
params={
    'userId': '32406500046',
    'password': '80d465bb3f55ad6d8f744e64b92303344ee60b73fb4ccdbdb0f594a8e4853875179d6ea8860d7edfe828691f2dd42985c7a1ef4ead1604b0125d680395c83103d8d2782474d752cbf5926012a050c2e589a08f40b3d7beef4a9d4fc02faa768baaade5684e357a3cf5aa9e9eb2a98d16d84ea034a086eb3005e554101d4ab73d',
    'service': '',
    'queryString': r'wlanuserip%3D172.26.201.76%26wlanacname%3DAC%26ssid%3DGZHU%252Dstudent%26mac%3DA4-42-CD-72-8F-B7%26url%3Dhttp%3A%2F%2F123.123.123.123%2F',
    'operatorPwd': '',
    'operatorUserId': '',
    'validcode': '',
    'passwordEncrypt': 'true'
}

resp=requests.post(url, headers=headers, params=params)
print(resp.text)