import sys
from io import BytesIO
import requests
from PIL import Image
from geopy.distance import geodesic as GD

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
    "format": "json"}
resp = requests.get(search_api_server, params=search_params)
if not resp:
    pass
json_resp = resp.json()
# Получаем первую найденную организацию.
organization = json_resp["features"][0]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]
org_hours = organization["properties"]["CompanyMetaData"]['Hours']['text']
# Получаем координаты ответа.
point = organization["geometry"]["coordinates"]
d = round(GD((float(toponym_longitude), float(toponym_lattitude)), (point[0], point[1])).m)
org_point = "{0},{1}".format(point[0], point[1])

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "l": "map",
    "pt": f'{coords},comma~{org_point},flag'}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(response.content)).show()
print('Название аптеки:', org_name)
print('Адрес:', org_address)
print('Время работы:', org_hours)
print('Расстояние до аптеки:', d, 'м')
