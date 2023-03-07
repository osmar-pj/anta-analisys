from main import login
from getResource import getResources

resources = getResources()


# def getZones():
sdk = login()
paramZones = {
    'itemId': resources['items'][0]['id'],
    'col': 1,
    'flags': 0x10
}
zones = sdk.resource_get_zone_data(paramZones)
    # df = pd.DataFrame(zones)
    # return zones
