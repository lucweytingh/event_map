import folium
import webbrowser
from pathlib import Path
from decouple import config


class LocationMapper:
    def __init__(self):
        """A class to make a map with markers"""
        self.map_fpath = Path(config("PROJECT_DIR")) / "map.html"
        self.map_obj = folium.Map()

    def create_map(self, names, descriptions, addresses, coordinates):
        """Creates a map from names, descriptions, addresses, and coordinates"""
        popups = self._create_popups(names, addresses, descriptions)
        self._add_markers(coordinates, popups)
        self.map_obj.fit_bounds(self._get_outer_coordinates(coordinates))
        self.map_obj.save(self.map_fpath)

    def open_map(self):
        """Open the map in a browser if it was created"""
        if self.map_fpath.is_file():
            webbrowser.open_new_tab(f"file://{self.map_fpath}")
            return
        print(
            "No map was created yet, use LocationMapper.create_map to create one "
        )

    def _add_markers(self, coordinates, popups):
        """Adds the given coordinates (with popups) to the map"""
        [
            folium.Marker(
                coord,
                popup=popup,
            ).add_to(self.map_obj)
            for coord, popup in zip(coordinates, popups)
            if coord
        ]

    @staticmethod
    def _get_outer_coordinates(coordinates):
        """Returns the min and max coordinate bounds as tuple"""
        lat = [x[0] for x in coordinates if x is not None]
        lon = [x[1] for x in coordinates if x is not None]
        return [(min(lat), min(lon)), (max(lat), max(lon))]

    @staticmethod
    def _create_popups(names, addresses, descriptions):
        """Creates html popups from the given names, addresses, and descriptions"""
        popups = [
            folium.Popup(
                f"<h4>{names[i]}</h4><h5>{addresses[i]}</h5><p>{descriptions[i]}</p>",
                max_width=3000,
            )
            for i in range(len(names))
        ]
        return popups
