from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ciscoaplookup',
    version="0.13.5",
    author="Steffen Schumacher",
    author_email="ssch@wheel.dk",
    description="The Cisco Wireless LAN Compliance Lookup library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/steffenschumacher/ciscoaplookup.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=['requests',
                      'beautifulsoup4',
                      'openpyxl==3.1.2',
                      'country_converter',
                      "python-dotenv",
                      "environs",
                      ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)