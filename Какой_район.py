import sys
import requests

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
coords = f'{toponym_longitude},{toponym_lattitude}'
search_params = {
    "apikey": apikey,
    "kind": "district",
    "geocode": coords,
    "format": "json"}
resp = requests.get(geocoder_api_server, params=search_params)
if not resp:
    pass
json_resp = resp.json()
d = json_resp["response"]["GeoObjectCollection"]['featureMember'][0]['GeoObject']
district = d['metaDataProperty']['GeocoderMetaData']['Address']['Components'][-1]['name']
print(district)
