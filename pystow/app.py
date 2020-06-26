#!/usr/bin/env python3


"""
-d DIR, --dir=DIR     Set stow dir to DIR (default is current dir)
-t DIR, --target=DIR  Set target to DIR (default is parent of stow dir)
-S, --stow            Stow the package names that follow this option
-D, --delete          Unstow the package names that follow this option
-R, --restow          Restow (like stow -D followed by stow -S)
-n, --no, --simulate  Do not actually make any filesystem changes
-V, --version         Show stow version number
-h, --help            Show this help
"""


import os
import sys
import getopt


def unlink(f):
    if os.path.islink(f):
        os.unlink(f)
    else:
        print(f, "is not a link")


def stow(directory=".", target="..", action="stow", simulate=False):

    print(directory)
    print(target)
    print(action)
    print(simulate)

    for root, dirs, files in os.walk(directory, followlinks=True):
        pass


def print_help():
    print("Help")


def main(argv):

    try:
        opts, args = getopt.getopt(
            argv,
            "d:t:DRShnv",
            [
                "dir=",
                "target=",
                "delete",
                "restow",
                "stow",
                "help"
                "no",
                "simulate",
                "version"
            ]
        )
    except getopt.GetoptError:
        print("Wrong combination of options or arguments")
        print_help()
        sys.exit(2)

    directory = "."
    target = ".."
    action = "stow"
    simulate = False

    for opt, arg in opts:

        if opt in ("-h", "--help"):
            print_help()
            sys.exit()

        elif opt in ("-v", "--verion"):
            sys.exit()

        elif opt in ("-d", "--dir"):
            directory = arg

        elif opt in ("-d", "--target"):
            target = arg

        elif opt in ("-n", "--no", "--simulate"):
            simulate = True

        elif opt in ("-D", "--delete"):
            action = "delete"

        elif opt in ("-R", "--restow"):
            action = "restow"

        elif opt in ("-S", "--stow"):
            action = "stow"

    stow(
        directory=directory,
        target=target,
        action=action,
        simulate=simulate
    )


if __name__ == "__main__":
    main(argv=sys.argv[1:])
