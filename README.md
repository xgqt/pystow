# PYStow

GNU Stow rewritten in python


# Dependencies

## Buildtime

- git (vcs)
- pip
- make (for user)

## Runtime

- python3.6 or higher


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
emerge --autounmask --noreplace --oneshot app-eselect/eselect-repository
eselect repository add myov git https://gitlab.com/xgqt/myov
emaint sync -r myov
emerge --autounmask --noreplace --verbose app-admin/pystow
```
