"""
Setup for flowsa package
"""

from setuptools import setup, find_packages

setup(
    name='flowsa',
    version='1.2.4',
    packages=find_packages(),
    package_dir={'flowsa': 'flowsa'},
    include_package_data=True,
    install_requires=[
        'fedelemflowlist @ git+https://github.com/USEPA/Federal-LCA-Commons-Elementary-Flow-List#egg=fedelemflowlist',
        'esupy @ git+https://github.com/USEPA/esupy#egg=esupy',
        'StEWI @ git+https://github.com/USEPA/standardizedinventories#egg=StEWI',
        'pandas>=1.4.0',
        'pip>=9',
        'setuptools>=41',
        'pyyaml>=5.3',
        'requests>=2.22.0',
        'appdirs>=1.4.3',
        'pycountry>=19.8.18',
        'xlrd>=2.0.1',
        'openpyxl>=3.0.7',
        'requests_ftp==0.3.1',
        'tabula-py>=2.1.1',
        'numpy>=1.20.1',
        'bibtexparser>=1.2.0',
        'python-dotenv >= 0.19.1',
        'seaborn>=0.11.2',
        'matplotlib>=3.4.3'
    ],
    url='https://github.com/USEPA/FLOWSA',
    license='MIT',
    author='Catherine Birney, Ben Young, Matthew Chambers, Melissa Conner, '
           'Jacob Specht, Mo Li, and Wesley Ingwersen',
    author_email='ingwersen.wesley@epa.gov',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: IDE",
        "Intended Audience :: Science/Research",
        "License :: MIT",
        "Programming Language :: Python :: 3.x",
        "Topic :: Utilities",
    ],
    description='Attributes resources (environmental, monetary, and human), '
                'emissions, wastes, and losses to US industrial and final '
                'use sectors.'
)
