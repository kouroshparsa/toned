"""
toned
-----------

toned is a search tool which allows boolean search operations

Link
`````

* Source
  https://github.com/kouroshparsa/

"""
from setuptools import Command, setup, find_packages

version = '1.1.0'
import sys
setup(
    name='toned',
    version=version,
    url='https://github.com/kouroshparsa/toned',
    download_url='https://github.com/kouroshparsa/toned/packages/%s' % version,
    license='GNU',
    author='Kourosh Parsa',
    author_email="kouroshtheking@gmail.com",
    description='a tool to allow boolean search operations on files',
    long_description=__doc__,
    packages=find_packages(),
    install_requires = [],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
