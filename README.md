# PYStow

GNU Stow rewritten in python


# Dependencies

## Buildtime

- git (vcs)
- pip
- make

## Runtime

- >=python3.6


# Installation

# Git

As user:

```sh
git clone --recursive --verbose https://gitlab.com/xgqt/pystow
cd pystow
make install
```


# Gentoo

As root:

```sh
emerge -1nv app-eselect/eselect-repository
eselect repository enable myov
emaint sync -r myov
emerge -av --autounmask app-admin/pystow
```
