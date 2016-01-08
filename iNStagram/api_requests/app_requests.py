__author__ = 'Freek, Zafer, Angelo'
__build__ = "versie 3.0"

import requests
import xmltodict

INFO_NS = {
    "url": "http://webservices.ns.nl/ns-api-stations-v2",
    "auth": ('freek.zandwijk@student.hu.nl', '0gZFU8fHjROwswm1XxvG5H4AY8LKVWwadMbc78h7T1J8n18hE6n5FQ')
}
INFO_INSTAGRAM = {
    "url": "https://api.instagram.com/v1/media/search?lat=%.6f&lng=%.6f&access_token=%s",
    "auth": "2371137240.1677ed0.f05412253449452f86d9a51828da4d7d"
}

# NS API request
def haal_stationgegevens_op():
    """
    Haalt de namen en locatie van alle stations uit de ns api
    :return: lijst van dicts met namen en locatie per station
    :rtype: list
    !dit zou je maar een keer hoeven te gebruiken want deze gegevens veranderen niet dus kan je ze opslaan
    """
    response = requests.get(INFO_NS["url"], auth=INFO_NS["auth"])
    if response.status_code == 200:  # als het verzoek succesvol is
        print("Stations ophalen...")
        stations_dict = xmltodict.parse(response.content)
        stations = stations_dict["Stations"]["Station"]
        stations_opslaan = []
        for station in stations:
            namen = dict(station["Namen"])
            locatie = (station["Lat"], station["Lon"])
            station_opslaan = {"namen": namen, "locatie": locatie}
            stations_opslaan.append(station_opslaan)

        return stations_opslaan
    else:
        print("ERROR", response.status_code)


# met deze functie hoef je de dict alleen door te geven
def request_iNS(station_dict):
    loc = station_dict["locatie"]
    return request_instagram(loc["lat"], loc["lon"])


#Instagram API request
def request_instagram(lat, lon):
    response = requests.get(INFO_INSTAGRAM["url"] % (lat, lon, INFO_INSTAGRAM["auth"]))
    if response.status_code == 200:
        import json

        content_dict = json.loads(response.content.decode('ascii'))
        medias = content_dict["data"]
        # print(json.dumps(medias,indent=4))
        instagram_medias = []
        for media in medias:

            created_time = int(media["created_time"])

            link = media["link"]
            soort = media["type"]

            instagram_media = {"tijd": created_time,
                            "link": link,
                            "type": soort}
            instagram_medias.append(instagram_media)
        return instagram_medias


    else:
        print("ERROR", response.status_code)


if __name__ == '__main__':
    instagram_medias = request_instagram(52.7338905334473, 6.47361087799072)
    for im in instagram_medias:
        print(im)
