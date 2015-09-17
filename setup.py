#!/usr/bin/env python
import cheesy
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup



setup(
    name='cheesy',
    description='cheesy gives you all the information for today\'s cheese shop pipy factory.',
    long_description=open('README.md').read(),
    classifiers=[],
    package_data={'': ['LICENSE.txt']},
    include_package_data=True,
    version=cheesy.__version__,
    author=cheesy.__author__,
    author_email=cheesy.__author_email__,
    maintainer=cheesy.__maintainer__,
    maintainer_email=cheesy.__maintainer_email__,
    url=cheesy.__url__,
    download_url = 'https://github.com/arindampradhan/cheesy/archive/v0.0.1.tar.gz',
    license='MIT',
    install_requires=[
        "requests",
        "docopt",
        "beautifulsoup4"
    ],
    keywords = ['pipy', 'information', 'packages'],
    packages=['cheesy'],
    entry_points={
        'console_scripts': [
            'cheesy = cheesy.ch:main',
        ]
    },
)