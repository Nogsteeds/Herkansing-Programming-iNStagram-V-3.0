__author__ = 'Freek, Zafer, Angelo'
__build__ = "versie 3.0"

from tkinter import *

from iNStagram.file_io.fileio import lees_stationgegevens
from iNStagram.api_requests.app_requests import request_instagram

import datetime
import webbrowser

startscherm = Tk()
startscherm.title('iNStagram media')
startscherm.minsize(width=790, height=600, )
startscherm.configure(bg='#2b6991')

e = Entry(master=startscherm, fg='#2f6d97')
e.place(x=35, y=440)

T = Text(startscherm, height=25, width=120, bd=5, bg='#2f6d97', fg='#dfebf4')

T.pack()


def openHLink(event):
    # Pas links aan zodat deze in een browser geopend kunnen worden.
    start, end = T.tag_prevrange("hlink",
                                 T.index("@%s,%s" % (event.x, event.y)))
    webbrowser.open_new(T.get(start, end))


T.tag_configure("hlink", foreground='#dfebf4', underline=1)
T.tag_bind("hlink", "<Control-Button-1>", openHLink)


def weergeef_instagram_links():
    """
    Geeft de bijbehorende station dict uit de lijst van alle stations (in de NS API)
    :param stationnaam: geef ofwel kort, middel als lange stationnaam om de bijbehorende station te identificeren
    :type stationnaam: str
    :return: station dict met namen en locatie
    :rtype: dict
    """
    T.delete(1.0, END)
    stationnaam = e.get()
    stations = lees_stationgegevens()
    gevonden = None
    for station in stations:

        if stationnaam in station["namen"].values():
            gevonden = stationnaam
            lat, lon = station["locatie"]
            lat = float(lat)
            lon = float(lon)
            instagram_data_dict = request_instagram(lat, lon)
            for data in instagram_data_dict:
                regeltekst = "%-20s %-60s" % (datetime.datetime.fromtimestamp(data["tijd"]), data["type"])

                T.insert(END, data["link"], "hlink", "       " + regeltekst + '\n')

    if gevonden is not None:
        print("Station %s gevonden" % gevonden)
    else:
        print("Geen station gevonden")
        T.insert(END, "Geen station gevonden")


b = Button(master=startscherm, text="Zoek op iNStagram", width=15, height=1, bg='#dfebf4', fg='#2f6d97',
           command=weergeef_instagram_links)
b.place(x=165, y=437)

startscherm.mainloop()
