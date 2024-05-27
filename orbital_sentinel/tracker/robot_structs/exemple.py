from skyfield.api import N,S,E,W, wgs84, load
ts = load.timescale()
t = ts.utc(1980, 1, 1)
planets = load('de421.bsp')
earth, mars = planets['earth'], planets['mars']
# Altitude and azimuth in the sky of a
# specific geographic location

boston = earth + wgs84.latlon(42.3583 * N, 71.0603 * W, elevation_m=43)
astro = boston.at(ts.utc(1980, 3, 1)).observe(mars)
app = astro.apparent()

alt, az, distance = app.altaz()
print(alt.dstr())
print(az.dstr())
print(distance)

altitude_degrees = alt.degrees
azimuth_degrees = az.degrees

t = Orbital_target_natural('mars')
t.compute_position(45, 3, 54)