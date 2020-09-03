#!/usr/bin/env python3


from setuptools import setup


def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='pystow',
    version='1.1',
    description='GNU Stow rewritten in Python',
    author='XGQT',
    author_email='xgqt@protonmail.com',
    url='https://gitlab.com/xgqt/pystow',
    long_description=readme(),
    long_description_content_type='text/markdown',
    license='GPL-3',
    keywords="stow",
    python_requires=">=3.6.*",
    packages=['pystow'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'pystow = pystow.app:main'
        ],
    },
    classifiers=[
        'Development Status :: Beta',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Bug Tracking',
    ]
)
