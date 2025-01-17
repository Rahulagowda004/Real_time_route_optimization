from setuptools import find_packages, setup
import os
from typing import List

def get_requirements(file_path:str)->List[str]:
    requirements = []
    with open(file_path) as file_obj:
        requirements = [req.strip() for req in file_obj.readlines() 
                      if req.strip() and not req.startswith('-e .')]
    return requirements

setup(
    name='real_time_route_optimization',
    version='0.0.1',
    author='RahulAGowda',
    author_email='rahulgowda277.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'matplotlib',
        'seaborn'
    ],
    description='Real-time route optimization package',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)