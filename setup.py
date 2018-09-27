import os

from setuptools import find_packages, setup

try:
    readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
except:
    readme = ''

version = '0.1'

install_requires = [
    'six>=1.9',
    'django-nine>=0.1.10',
]

extras_require = []

tests_require = [
    'factory_boy',
    'fake-factory',
    'pytest',
    'pytest-django',
    'pytest-cov',
    'tox'
]

setup(
    name='muses',
    version=version,
    description="Central place (API) to search/browse through various "
                "museum collections",
    long_description=readme,
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Environment :: Web Environment",
        "License :: OSI Approved :: Apache Software License",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    keywords="museum, images, object detection, api",
    author='Goldmund, Wyldebeast & Wunderliebe',
    author_email='info@gw20e.com',
    url='https://github.com/aincient/cleo/',
    package_dir={'': 'src'},
    packages=find_packages(where='./src'),
    license='GPL 2.0/LGPL 2.1',
    install_requires=(install_requires + extras_require),
    tests_require=tests_require,
    include_package_data=True,
)
