__author__ = 'Freek, Zafer, Angelo'
__build__ = "versie 3.0"

from iNStagram.api_requests.app_requests import haal_stationgegevens_op
import os

bestandnaam_stations="../file_io/stations.txt" # het is relatief aan de file .../file_io/. <- je bent hier

def sla_stationsgegevens_op(alleen_als_niet_bestaat=False):
    """
    Slaat de stationsgegevens op in een bestand
    :param alleen_als_niet_bestaat: zorgt ervoor dat er allen wordt opgeslagen als het bestand niet bestat
    :type alleen_als_niet_bestaat: bool
    :param bestandnaam: bestandsnaam waarin de stations worden opgeslagen
    :return:
    """
    if alleen_als_niet_bestaat and os.path.exists(bestandnaam_stations):
        print("bestond al")
        return
    stationsgegevens = haal_stationgegevens_op()
    print("Stations opslaan...")
    with open(bestandnaam_stations,"w") as stations_bestand:
        for station in stationsgegevens:
            stations_bestand.write(str(station)+"\n")
    #with open sluit de bestand.close() als de blok eindigd

def lees_stationgegevens():
    """
    Leest de stationsgegevens uit het (lokaal) opgeslagen bestand, dit scheelt want je hoeft dan niet steeds verbinding met de ns api te maken
    :return: lijst van dicts met namen en locatie per station
    :rtype: list
    """
    from ast import literal_eval
    stations = []
    print("Stations lezen...")
    with open(bestandnaam_stations,"r") as stations_bestand:
        for regel in stations_bestand.readlines():
            station_dict = literal_eval(regel)
            stations.append(station_dict)


    return stations

if __name__ == '__main__':
    sla_stationsgegevens_op(True)
    lees_stationgegevens()