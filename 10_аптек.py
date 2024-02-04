import sys
from io import BytesIO
import requests
from PIL import Image

toponym_to_find = " ".join(sys.argv[1:])
apikey = "40d1649f-0493-4b70-98ba-98533de7710b"

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": apikey,
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym.split(" ")
search_api_server = "https://search-maps.yandex.ru/v1/"
coords = f'{toponym_longitude},{toponym_lattitude}'
search_params = {
    "apikey": 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
    "text": "аптека",
    "lang": "ru_RU",
    "ll": coords,
    "format": "json",
    'results': 10}
resp = requests.get(search_api_server, params=search_params)
if not resp:
    pass
lt = []
json_resp = resp.json()
for i in json_resp['features']:
    organization = i
    org_hours = organization["properties"]["CompanyMetaData"]['Hours']['text']
    point = organization["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])
    if 'круглосуточно' in org_hours:
        lt.append(org_point + ",pm2gnm")
    elif org_hours:
        lt.append(org_point + ",pm2blm")
    else:
        lt.append(org_point + ",pm2grm")

map_params = {
    "l": "map",
    "pt": "~".join(lt)}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(response.content)).show()