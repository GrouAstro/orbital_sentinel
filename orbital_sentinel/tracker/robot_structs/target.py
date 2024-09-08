from skyfield.api import EarthSatellite, load, wgs84, Topos
import math as m
from time import sleep


class Orbital_target_natural:

    def __init__(self, id_body: str):

        self.ts = load.timescale()
        self.id = id_body
        self.visibility = 0
        self.velocity = 0
        self.azimuth = 0
        self.elevation = 0
        self.distance = 0
        self.target_mod = 0
        self.type_name = 'init'
        self.ephemeris = load('de421.bsp')

    def change_target(self, new_target: str):
        """

        Args:
            new_target:

        Returns:

        """

        table = {'mercury', 'venus', 'earth',
                 'mars', 'jupiter barycenter', 'saturn barycenter',
                 'uranus barycenter', 'neptune barycenter', 'pluto barycenter', 'moon'}

        if new_target in table:
            print('New target : ', new_target)
            self.id = new_target  # TO DO add barycentre

        else:
            print('Incorrect please use an other one')

    def compute_position(self, lat: float, lon: float, alt: float):
        """

        Args:
            lat:
            lon:
            alt:

        Returns:

        """

        t = self.ts.now()
        eph_target = self.ephemeris[self.id]
        current_location = self.ephemeris['earth'] + wgs84.latlon(lat, lon, elevation_m=alt)
        astro = current_location.at(t).observe(eph_target)
        app = astro.apparent()

        alt, az, distance = app.altaz()
        self.azimuth = az.degrees
        self.elevation = alt.degrees
        self.distance = distance

        if alt.degrees > 0:
            self.visibility = 1
        else:
            self.visibility = 0

        # data_pos = [self.azimuth, self.elevation, self.distance]

        return

    def print_name(self):
        """

        Returns:

        """
        print(self.id)

    def get_name(self):
        """

        Returns:

        """

        return self.id

    def print_azimuth(self):
        """

        Returns:

        """
        print(self.azimuth)

    def get_azimuth(self):
        """

        Returns:

        """
        return self.azimuth

    def print_elevation(self):
        """

        Returns:

        """
        print(self.elevation)

    def get_elevation(self):
        """

        Returns:

        """
        return self.elevation

    def print_distance(self):
        """

        Returns:

        """
        print(self.distance)

    def get_distance(self):
        """

        Returns:

        """
        return self.distance

    def get_position(self):
        """

        Returns:

        """
        print('Azimuth : ', round(self.azimuth, 2),
              ' | Elevation : ', round(self.elevation, 2))

    def print_visibility(self):
        """

        Returns:

        """
        if self.visibility == 1:
            print('Target in the sky')
        else:
            print('Target not available')

    def get_visibility(self):
        """

        Returns:

        """
        return self.visibility

    def tracking_data(self, lat: float, lon: float, alt: float):
        """

        Args:
            lat:
            lon:
            alt:

        Returns:

        """

        while True:

            try:
                self.compute_position(lat, lon, alt)
                self.get_position()
                sleep(0.05)

            except KeyboardInterrupt:
                print('Stop tracking mod')
                break
