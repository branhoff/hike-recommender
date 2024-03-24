import osmnx as ox


def address2latlon(target_address):
    '''
    Convert address into lat/lon using openstreetMap geocoding function
    '''
    # Geocode the target address to get its latitude and longitude
    target_location = ox.geocode(target_address)
    lat = target_location[0]
    lon = target_location[1]
    return lat, lon

if __name__ =="__main__":
    address = "1600 Amphitheatre Parkway, Mountain View, CA"
    print(address2latlon(address))