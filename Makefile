# This file is part of pystow.

# pystow is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pystow is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pystow.  If not, see <https://www.gnu.org/licenses/>.

# Copyright (c) 2020-2021, Maciej Barć (xgqt@protonmail.com)
# Licensed under the GNU GPL v3 License


BIN = pystow


.PHONY: all clean install uninstall distclean


all:
	@echo did nothing. try targets: install, or uninstall.


clean:
	$(RM) -dr $(BIN).egg-info
	$(RM) -dr build
	$(RM) -dr dist
	$(RM) -dr $(BIN)/__pycache__


install:
	python setup.py -v install --user


uninstall:
	pip uninstall -v -y $(BIN)


distclean: uninstall
distclean: clean
