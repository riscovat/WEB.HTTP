import sys
from io import BytesIO
import requests
from PIL import Image

toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")


def delt(toponym):
    d1 = list(map(float, toponym["boundedBy"]["Envelope"]['lowerCorner'].split()))
    d2 = list(map(float, toponym["boundedBy"]["Envelope"]['upperCorner'].split()))
    delta1 = str(abs(d1[0] - d2[0]))
    delta2 = str(abs(d1[1] - d2[1]))
    return (delta1, delta2)


delta1, delta2 = delt(toponym)

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta1, delta2]),
    "l": "map",
    "pt": "{},pm2rdm".format(",".join([toponym_longitude, toponym_lattitude]))}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(response.content)).show()
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы
