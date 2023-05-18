from src.location_mapper import LocationMapper
from src.echtzeitmusik import EchtZeitMusik


ezm = EchtZeitMusik()
lm = LocationMapper()

names, descriptions, addresses, coordinates = ezm.get_events()

lm.create_map(names, descriptions, addresses, coordinates)
lm.open_map()
