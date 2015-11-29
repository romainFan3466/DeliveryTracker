
from application.classes.Location import Location


def address_to_geocode():
    addr = "850 Avenue de Londres, Z.A.C du Grand Saint Charles, 66000 Perpignan, FR"

    geo = Location.getGeocode(addr=addr)
    print(geo)

def geocode_to_address():
    addr = Location.getGeocode(lat=52.370402, lng=4.894948)
    print(addr)

geocode_to_address()
