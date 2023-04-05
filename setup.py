#!/usr/bin/env python3


"""
This file is part of pystow.

pystow is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.

pystow is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pystow.  If not, see <https://www.gnu.org/licenses/>.

Copyright (c) 2020-2021, Maciej Barć <xgqt@riseup.net>
Licensed under the GNU GPL v3 License
"""


from setuptools import setup


def readme():
    """use README.md as the long_description"""
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setup(
    name="pystow",
    version="1.2.2",
    description="GNU Stow rewritten in Python",
    author="Maciej Barć",
    author_email="xgqt@riseup.net",
    url="https://gitlab.com/xgqt/pystow",
    long_description=readme(),
    long_description_content_type="text/markdown",
    license="GPL-3",
    keywords="stow",
    packages=["pystow"],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "pystow = pystow.app:main"
        ],
    },
    classifiers=[
        "Development Status :: Beta",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Communications :: Email",
        "Topic :: Software Development :: Bug Tracking",
    ]
)
