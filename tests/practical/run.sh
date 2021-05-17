#!/bin/sh


# This file is part of pystow.

# pystow is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.

# pystow is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pystow.  If not, see <https://www.gnu.org/licenses/>.

# Copyright (c) 2021, Maciej Barć (xgqt@riseup.net)
# Licensed under the GNU GPL v3 License


# Prepare

[ -d ./target ] && rm -r ./target

mkdir -p ./target

mkdir -p ./target/d1/


# Stow

python3 ../../pystow/app.py \
        -d ./dir \
        -t ./target \
        -S -v \
        "$(pwd)"/dir/*


# Show the results

tree -a || return 0
