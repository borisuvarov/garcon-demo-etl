"""Setup Demo ETL project."""

from setuptools import find_packages
from setuptools import setup


setup(
    name='etl_demo',
    version='0.1',
    description='Demo ETL project',
    packages=find_packages(),
    include_package_data=True,
    entry_points=dict(console_scripts=['garcon = cli:garcon'])
)
