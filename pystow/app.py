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


def stow(directory=".", target="..", action="stow", simulate=False, verbose=False):

    if verbose:
        print(
            "Options:",
            "\n", "- Directory:", directory,
            "\n", "- Target:", target,
            "\n", "- Action:", action,
            "\n", "- Simulate:", simulate,
            "\n"
        )

        def linker(d, t):
            for inside in os.listdir(d):
                if os.path.isfile(t + "/" + inside) or os.path.islink(t + "/" + inside):
                    print("File", t + "/" + inside, "already exists")
                elif os.path.isdir(t + "/" + inside):
                    linker(d + "/" + inside, t + "/" + inside)
                else:
                    if action == "stow":
                        if simulate:
                            print("Will link " + d + "/" + inside + " to " + t + "/")
                        else:
                            os.symlink(d + "/" + inside, t + "/" + inside)

        if directory == ".":
            for inside in os.listdir(directory):
                for inside in os.listdir(directory):
                    if os.path.isdir(inside) and not inside[0] == ".":
                        linker(inside, target)
        else:
            linker(directory, target)


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
    verbose = False

    for opt, arg in opts:

        if opt in ("-h", "--help"):
            print_help()
            sys.exit()

        elif opt in ("-V", "--verion"):
            sys.exit()

        elif opt in ("-d", "--dir"):
            directory = arg

        elif opt in ("-t", "--target"):
            target = arg

        elif opt in ("-n", "--no", "--simulate"):
            simulate = True

        elif opt in ("-v", "--verbose"):
            verbose = True

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
        simulate=simulate,
        verbose=verbose
    )


if __name__ == "__main__":
    main(argv=sys.argv[1:])
