from skyfield.api import EarthSatellite, load, wgs84, Topos
#from orbital_sentinel.tracker.robot_structs.tracker import Tracker
import math as m
import types


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

    def compute_position(self, lat, lon, alt):

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

    def get_azimuth(self):
        print(self.azimuth)

    def get_elevation(self):
        print(self.elevation)

    def get_visibility(self):
        if self.visibility == 1:
            print('Target in the sky')
        else:
            print('Target not available')


class Orbital_target_earth:

    def __init__(self, tle_info):
        self.ts = load.timescale()
        self.info = list(tle_info)
        self.velocity = 0
        self.altitude = 0
        self.longitude = 0
        self.latitude = 0
        self.target_mod = 0
        self.type_name = 'init'
        self.type_id = tle_info[0]

    # def change_target(self, new_target):

    def compute_geo_pos(self):
        t = self.ts.now()
        eph_sat = EarthSatellite(self.info[1], self.info[2], self.type_id, self.ts)
        geocentric = eph_sat.at(t)
        self.latitude, self.longitude = wgs84.latlon_of(geocentric)
        xyz = geocentric.position.km
        self.altitude = m.sqrt(xyz[0] ** 2 + xyz[1] ** 2 + xyz[2] ** 2) - 6378

    def get_geo_pos(self):
        print(self.latitude)
        print(self.longitude)
        print(self.altitude)