#!/usr/bin/env python3


from os import walk
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
    for (dirpath, dirnames, filenames) in walk(args.dir):
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
        print(" -", "Dir:", os.path.abspath(args.dir))
        print(" -", "Target:", os.path.abspath(args.target))
        print(" -", "Packages:", args.pkgs)
        print(" -", "Simulate?", args.simulate)
        print(" -", "Stow?", args.stow)
        print(" -", "Delete?", args.delete)
        print(" -", "Restow?", args.restow)

    for pkg in args.pkgs:

        if args.verbose:
            print("Package:", pkg)

        for (dirpath, dirnames, filenames) in walk(args.dir + "/" + pkg):

            wanted = os.path.abspath(args.target) + dirpath.replace(os.path.abspath(args.dir + "/" + pkg), "")
            if args.verbose:
                print("Wanted:", wanted)

            objects = dirnames + filenames
            if args.verbose:
                print("Objects:", objects)

            for obj in objects:

                if args.stow and not os.path.exists(wanted + "/" + obj):
                    os.chdir(wanted)
                    relpath = os.path.relpath(dirpath + "/" + obj)
                    if args.verbose:
                        print(relpath, "->", obj)
                    if not args.simulate:
                        os.symlink(relpath, obj)

                elif args.delete and os.path.islink(wanted + "/" + obj):
                    if args.verbose:
                        print(dirpath + "/" + obj, "<>", wanted + "/" + obj)
                    if not args.simulate:
                        os.unlink(wanted + "/" + obj)

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
