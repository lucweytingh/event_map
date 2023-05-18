import requests
import re
from geopy.geocoders import Nominatim
from decouple import config
from bs4 import BeautifulSoup


class EchtZeitMusik:
    def __init__(self):
        """A class for scraping echtzeitmusik.de for today's events"""
        self.calendar_href = "https://echtzeitmusik.de/index.php?page=calendar"
        self.geolocator = None
        self.page = None

        self.names = None
        self.descriptions = None
        self.addresses = None
        self.coordinates = None

    def get_events(self):
        """
        Returns lists of names, descriptions, addresses, and coordinates of
        today's events
        """
        names = self.get_names()
        descriptions = self.get_descriptions()
        addresses = self.get_addresses()
        coordinates = self.get_coordinates()
        return names, descriptions, addresses, coordinates

    def get_names(self):
        """Returns a list of event space names"""
        if self.names is not None:
            return self.names

        names = self._get_page().find_all("td", attrs={"class": "name-box"})
        self.names = [x.text.strip() for x in names]
        return self.names

    def get_descriptions(self):
        """Returns a list of descriptions for the events"""
        if self.descriptions is not None:
            return self.descriptions

        descriptions = self._get_page().find_all(
            "div", attrs={"class": "calender-entry-info"}
        )
        self.descriptions = [x.decode_contents().strip() for x in descriptions]
        return self.descriptions

    def get_addresses(self):
        """Returns a list of addresses for the events"""
        if self.addresses is not None:
            return self.addresses

        addresses = self._get_page().find_all(
            "div", attrs={"class": "calender-entry-address"}
        )
        self.addresses = [
            x.text.strip().replace("\r\n", ",") for x in addresses
        ]
        return self.addresses

    def get_coordinates(self):
        """Returns latitudes and longitudes for the events"""
        if self.coordinates is not None:
            return self.coordinates

        addresses = self.get_addresses()

        coordinates = []
        calendar_entries = self._get_page().find_all(
            "div", attrs={"class": "calender-entry-icons"}
        )
        for i, entry in enumerate(calendar_entries):
            link = entry.find(
                "a", attrs={"alt": "Google Maps", "class": "entry-info"}
            )
            if link is None:
                coordinates.append(self._get_lat_lon_by_address(addresses[i]))
            else:
                coordinates.append(self._extract_lat_lon_from_link(link))

        self.coordinates = coordinates
        return self.coordinates

    def _get_page(self):
        """Return the scraped EZM page (BeautifulSoup object)"""
        if self.page is not None:
            return self.page

        self.page = self._do_scrape()
        return self.page

    def _do_scrape(self):
        """Scrape echtzeitmusik page for today's events"""
        form_data = {"calendar_filter": "today"}
        response = requests.post(self.calendar_href, data=form_data)
        return BeautifulSoup(response.content, features="html.parser")

    def _get_geolocator(self):
        if self.geolocator is not None:
            return self.geolocator
        self.geolocator = Nominatim(user_agent="my_app")
        return self.geolocator

    @staticmethod
    def _extract_lat_lon_from_link(link):
        """Extract the latitude and longitude from a google maps link"""
        return tuple(
            map(
                float,
                link.get("href").split("/")[6][1:].split(",")[:2],
            )
        )

    def _get_lat_lon_by_address(self, address):
        """Find the coordinates for a given address"""
        located = self._get_geolocator().geocode(
            re.sub(r"\(.+?\),? ?", "", address)
        )
        return (located.latitude, located.longitude) if located else None
