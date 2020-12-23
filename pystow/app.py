#!/usr/bin/env python3


import argparse
import os


parser = argparse.ArgumentParser(
    description="GNU Stow rewritten in Python",
    epilog="Copyright (c) 2020, XGQT (License: GNU GPL Version 3)"
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


def main():
    if args.verbose:
        print("Running with options:")
        print(" - Directory : {}".format(os.path.abspath(args.dir)))
        print(" - Target    : {}".format(os.path.abspath(args.target)))
        print(" - Packages  : {}".format(args.pkgs))
        print(" - Simulate? : {}".format(args.simulate))
        print(" - Stow?     : {}".format(args.stow))
        print(" - Delete?   : {}".format(args.delete))
        print(" - Restow?   : {}".format(args.restow))

    for pkg in args.pkgs:

        if args.verbose:
            print("Package : {}".format(pkg))

        dir_pkg = os.path.join(args.dir, pkg)
        for (dirpath, dirnames, filenames) in os.walk(dir_pkg):

            wanted = os.path.abspath(args.target) + dirpath.replace(os.path.abspath(dir_pkg), "")

            if args.verbose:
                print("Wanted : {}".format(wanted))

            objects = dirnames + filenames
            if args.verbose:
                print("Objects : {}".format(objects))

            for obj in objects:
                wanted_obj = os.path.join(wanted, obj)

                if args.stow and not os.path.exists(wanted_obj):
                    os.chdir(wanted)
                    relpath = os.path.relpath(os.path.join(dirpath, obj))
                    if args.verbose:
                        print("{} -> {}".format(relpath, obj))
                    if not args.simulate:
                        os.symlink(relpath, obj)

                elif args.delete and os.path.islink(wanted_obj):
                    if args.verbose:
                        print("{}/{} <> {}/{}".format(
                            dirpath, obj, wanted, obj
                        ))
                    if not args.simulate:
                        os.unlink(wanted_obj)

                elif args.restow:
                    args.stow = False
                    args.delete = True
                    args.restow = False
                    main()
                    args.stow = True
                    args.delete = False
                    args.restow = False
                    main()


if __name__ == "__main__":
    main()
