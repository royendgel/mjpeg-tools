import os
from setuptools import setup

setup(
    name = "mjpeg-tools",
    version = "0.0.13",
    author = "Royendgel Silberie",
    author_email = "royendgel@techprocur.com",
    description = ("mjpeg client, server and manipulator"),
    keywords = "mjpegtools mjpeg jpeg",
    url = "https://github.com/royendgel",
    packages=['mjpegtools'],
    classifiers=[
      'Operating System :: MacOS :: MacOS X',
      'Operating System :: Unix',
      'Development Status :: 3 - Alpha',
      'Topic :: Utilities',
      'Programming Language :: Python :: 2.7',
    ],
    include_package_data=True,
    install_requires=[
      'pillow',
    ],
)
