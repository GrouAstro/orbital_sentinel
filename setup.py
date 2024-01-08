from setuptools import setup

setup(
    name="orbital_sentinel",
    version="0.1",
    description="",
    author="OLLIVIER Roman",
    author_email="roman.ollivier@outlook.fr",
    packages=["orbital_sentinel"],
    install_requires=[
        "wheel",
        "Sphinx>=4.5",
        "numpy >= >= 1.14.5,<2.0.0",
        "scipy",
        "pyserial",  
        "RPi.GPIO",
        "toml"

    ],
    extras_require=extras_require,
    python_requires=">=3.9, < 4",
)