#!/usr/bin/env python3


"""
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

# Copyright (c) 2020-2021, Maciej Barć (xgqt@riseup.net)
# Licensed under the GNU GPL v3 License
"""


import argparse
import os


parser = argparse.ArgumentParser(
    description="GNU Stow rewritten in Python",
    epilog="Copyright (c) 2020-2021, Maciej Barć (License: GNU GPL Version 3)"
)
group = parser.add_mutually_exclusive_group()

parser.add_argument(
    "-d", "--dir",
    type=str, default=".",
    help="Set stow directory (default is current dir)"
)
parser.add_argument(
    "-t", "--target",
    type=str, default="..",
    help="Set target directory (default is parent of stow dir)"
)
parser.add_argument(
    "-n", "--simulate",
    action="store_true",
    help="Do not actually make any filesystem changes"
)
parser.add_argument(
    "-v", "--verbose",
    action="store_true",
    help="Be verbose"
)
group.add_argument(
    "-S", "--stow",
    action="store_true",
    help="Stow the packages"
)
group.add_argument(
    "-D", "--delete",
    action="store_true",
    help="Unstow the packages"
)
group.add_argument(
    "-R", "--restow",
    action="store_true",
    help="Like stow -D followed by stow -S"
)
parser.add_argument(
    "pkgs",
    nargs="*",
    type=str
)

args = parser.parse_args()


def print_options():
    """Prnt arguments/options."""

    print("Running with options:")
    print(" - Directory : {}".format(os.path.abspath(args.dir)))
    print(" - Target    : {}".format(os.path.abspath(args.target)))
    print(" - Packages  : {}".format(args.pkgs))
    print(" - Simulate? : {}".format(args.simulate))
    print(" - Stow?     : {}".format(args.stow))
    print(" - Delete?   : {}".format(args.delete))
    print(" - Restow?   : {}".format(args.restow))


# If 'pkgs' is empty: append all non-hidden dirs to it
if args.pkgs == []:
    p = []
    for (dirpath, dirnames, filenames) in os.walk(args.dir):
        for p_ in dirnames:
            if not p_.startswith("."):
                p.append(p_)
        break
    args.pkgs = p

# Default action: stow
if not args.stow and not args.delete and not args.restow:
    args.stow = True

# Convert to absolute paths
args.dir = os.path.abspath(args.dir)
args.target = os.path.abspath(args.target)


def stow():
    """
    Stow or un-stow (delete).
    """

    for pkg in args.pkgs:

        if args.verbose:
            print("Package : {}".format(pkg))

        dir_pkg = os.path.join(args.dir, pkg)
        for (dir_path, dir_names, file_names) in os.walk(dir_pkg):

            wanted = args.target + dir_path.replace(dir_pkg, "")

            if args.verbose:
                print("Wanted : {}".format(wanted))

            objects = dir_names + file_names
            if args.verbose:
                print("Objects : {}".format(objects))

            for obj in objects:
                wanted_obj = os.path.join(wanted, obj)

                if args.stow and not os.path.exists(wanted_obj):
                    os.chdir(wanted)
                    relpath = os.path.relpath(os.path.join(dir_path, obj))
                    if args.verbose:
                        print("{} -> {}".format(relpath, obj))
                    if not args.simulate:
                        os.symlink(relpath, obj)

                elif args.delete and os.path.islink(wanted_obj):
                    if args.verbose:
                        print("{}/{} <> {}/{}".format(
                            dir_path, obj, wanted, obj
                        ))
                    if not args.simulate:
                        os.unlink(wanted_obj)


def main():
    """
    The main function.
    """

    if args.verbose:
        print_options()

    if args.restow:
        args.stow = False
        args.delete = True
        args.restow = False
        stow()
        args.stow = True
        args.delete = False
        args.restow = False
        stow()
    else:
        stow()


if __name__ == "__main__":
    main()
