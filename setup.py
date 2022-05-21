#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='wompi',
    version='1.0.0',
    author='Preki',
    author_email='ramos@preki.com',
    packages=['wompi', 'wompi.models', 'wompi.utils'],
    url='https://preki.com',
    download_url='https://github.com/GoPreki/WompiSDK',
    license='MIT',
    description='Python library for handling Wompi integration',
    long_description='Python library for handling Wompi integration',
    install_requires=[
        'requests >= 2.24.0',
    ],
)