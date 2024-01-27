from skyfield.api import load


def load_ephermeris():

    planets = load('de421.bsp')

    return planets
