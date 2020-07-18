#!/usr/bin/env python3


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
        for i in os.listdir(d):
            if verbose:
                print(d + "/" + i, t + "/" + i)
            if os.path.isfile(t + "/" + i) or os.path.islink(t + "/" + i):
                print("File", t + "/" + i, "already exists")
            elif os.path.isdir(t + "/" + i):
                linker(d + "/" + i, t + "/" + i)
            else:
                if simulate:
                    print("Will link " + d + "/" + i + " to " + t + "/" + i)
                else:
                    os.symlink(
                        os.path.abspath(d + "/" + i),
                        t + "/" + i
                    )

    def unlinker(d, t):
        for i in os.listdir(d):
            if verbose:
                print(d + "/" + i, t + "/" + i)
            if os.path.islink(t + "/" + i):
                if simulate:
                    print("Will remove " + t + "/" + i)
                else:
                    os.unlink(t + "/" + i)
            elif os.path.isfile(t + "/" + i):
                print("File", t + "/" + i, "already exists")
            elif os.path.isdir(t + "/" + i):
                unlinker(d + "/" + i, t + "/" + i)

    if action == "stow":
        if directory == ".":
            for inside in os.listdir(directory):
                if os.path.isdir(inside) and not inside[0] == ".":
                    linker(inside, target)
        else:
            linker(directory, target)
    elif action == "unstow":
        if directory == ".":
            for inside in os.listdir(directory):
                if os.path.isdir(inside) and not inside[0] == ".":
                    unlinker(inside, target)
        else:
            unlinker(directory, target)
    elif action == "restow":
        stow(
            directory=directory,
            target=target,
            action="unstow",
            simulate=simulate,
            verbose=verbose
        )
        stow(
            directory=directory,
            target=target,
            action="stow",
            simulate=simulate,
            verbose=verbose
        )


def print_help():
    print(
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
    )


def main(argv):

    try:
        opts, args = getopt.getopt(
            argv,
            "d:t:DRShnVv",
            [
                "dir=",
                "target=",
                "delete",
                "restow",
                "stow",
                "help"
                "no",
                "simulate",
                "version",
                "verbose"
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
            action = "unstow"

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
