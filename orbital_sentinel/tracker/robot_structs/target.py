from skyfield.api import EarthSatellite, load, wgs84, Topos
import math as m


class Orbital_target:

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
