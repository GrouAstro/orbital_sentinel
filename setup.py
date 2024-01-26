import os
from setuptools import setup, find_namespace_packages

if os.path.exists("README.md"):
    long_description = open("README.md").read()
else:
    long_description = 'This repository host files for robotics, aerodynamics and RF projects'\
                        'Only available on raspberry 3 and 4.'

setup(
    name="orbital_sentinel",
    version="0.1",
    description="",
    author="OLLIVIER Roman",
    author_email="roman.ollivier@outlook.fr",
    packages=find_namespace_packages(include=["tracker.robot_structs.*"]),
    install_requires=[
        "wheel",
        "Sphinx>=4.5",
        "numpy >= 1.14.5,<2.0.0",
        "scipy",
        "pyserial",  
        "RPi.GPIO",
        "toml",
        "pyserial"

    ],

    python_requires=">=3.9, < 4",
)