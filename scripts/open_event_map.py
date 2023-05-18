from src.location_mapper import LocationMapper
from src.echtzeitmusik import EchtZeitMusik

ezm = EchtZeitMusik()
names, descriptions, addresses, coordinates = ezm.get_events()

lm = LocationMapper()
lm.create_map(names, descriptions, addresses, coordinates)
lm.open_map()
