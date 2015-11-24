import googlemaps

from application import app

class Location:

    latitude = ""
    longitude = ""

    # addr = "850 Avenue de Londres, Z.A.C du Grand Saint Charles, 66000 Perpignan, FR"
    __gmaps = googlemaps.Client(key=app.config["GOOGLE_MAPS_KEY"])

    def __init__(self, addr=None, lat=None, long=None):

        if addr is not None:
            geocode = self.getGeocode(addr)
        self.latitude = geocode["lat"] if geocode["lat"] is not None else ""
        self.longitude = geocode["lgn"] if geocode["lgn"] is not None else ""


    @staticmethod
    def getGeocode(addr:str):
        geocode = Location.__gmaps.geocode(addr)
        # return { "lat":geocode[]}
        result = None
        if (
            len(geocode)>0 and
            "geometry" in geocode[0] and
            "location" in geocode[0]["geometry"] and
            ("lat" and "lng" in  geocode[0]["geometry"]["location"])
            ):

            result = geocode[0]["geometry"]["location"]

        return result


    @staticmethod
    def getGeocode(lat, lng ):
        geocode = Location.__gmaps.reverse_geocode((lat,lng))
        # return { "lat":geocode[]}
        # result = None
        # if (
        #     len(geocode)>0 and
        #     "geometry" in geocode[0] and
        #     "location" in geocode[0]["geometry"] and
        #     ("lat" and "lng" in  geocode[0]["geometry"]["location"])
        #     ):
        #
        #     result = geocode[0]["geometry"]["location"]


        return geocode





