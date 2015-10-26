import googlemaps

key = "AIzaSyBZjQHj564q5uyAyWNyh7cK6heAMoVZlvM"
addr = "850 Avenue de Londres, Z.A.C du Grand Saint Charles, 66000 Perpignan, FR"

gmaps = googlemaps.Client(key=key)

# Geocoding and address
geocode_result = gmaps.geocode(addr)

print(geocode_result)





class Location:

    latitude = ""
    longitude = ""

    def __init__(self, lat, long):
        self.latitude = lat
        self.longitude = long

