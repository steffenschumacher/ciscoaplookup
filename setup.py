from setuptools import setup, find_packages
desc = "The Cisco Wireless LAN Compliance Lookup library"

setup(
    name='ciscoaplookup',
    version="0.9.0",
    author="Steffen Schumacher",
    author_email="ssch@wheel.dk",
    description=desc,
    long_description=desc,
    long_description_content_type="text/markdown",
    url="https://github.com/steffenschumacher/ciscoaplookup.git",
    packages=find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    include_package_data=True,
    install_requires=['requests', 'xlrd'],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)