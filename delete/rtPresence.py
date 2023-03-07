from importlib import resources
import pandas as pd
from main import login
from getResource import getResources
from getUnit import getUnits
from getZones import getZones

resources = getResources()
units = getUnits()
zones = getZones()

sdk = login()
parameterSetLocale = {
    'tzOffset': -18000,
    "language": "en"
}

sdk.render_set_locale(parameterSetLocale)

paramUbication = {
    'spec': [{'type': 'col', 'data': [units['items'][0]['id']], 'flags': 4194304, 'mode': 0}]
}
resUbication = sdk.core_update_data_flags(paramUbication)

lat = resUbication[0]['d']['pos']['y']
lon = resUbication[0]['d']['pos']['x']

# PRESENCE IN GEOFENCE
paramPresence = {
    'spec': {
        'lat': lat,
        'lon': lon,
        'zoneId': {resources['items'][0]['id']: [1]}
    }
}

resPresence = sdk.resource_get_zones_by_point(paramPresence)
resourceId = resources['items'][0]['id']
zoneId = resPresence[str(resourceId)]
# zonesFiltered = zones.query("id == @zoneId")
print(zoneId)
