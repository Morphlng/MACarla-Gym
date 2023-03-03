#!/usr/bin/env python

from setuptools import setup, find_packages
import os

# Prepare long description using existing docs
long_description = ""
this_dir = os.path.abspath(os.path.dirname(__file__))
doc_files = ["README.md"]
for doc in doc_files:
    with open(os.path.join(this_dir, doc), 'r') as f:
        long_description = "\n".join([long_description, f.read()])
# Replace relative path to images with Github URI
github_uri_prefix = "https://raw.githubusercontent.com/praveen-palanisamy" \
                    "/macad-gym/master/"
rel_img_path = "docs/images/"
long_description = long_description.replace(
    "(" + rel_img_path, "(" + github_uri_prefix + rel_img_path)

setup(
    name="macarla-gym",
    version='0.1.0',
    description='A Gym environment for multi-agent RL training in CARLA',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Morphlng/MACarla-Gym',
    author='Morphlng',
    author_email='morphlng@proton.me',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=[
        'gym', 'carla>=0.9.13', 'GPUtil', 'pygame', 'opencv-python', 'networkx', 'numpy<=1.23.4', 'py_trees', 'shapely'
    ],
    extras_require={'test': ['tox', 'pytest', 'pytest-xdist',
                             'tox'], 'ray': ['ray==1.8.0', 'ray[tune]', 'ray[rllib]']},
    keywords='multi-agent learning environments'
    'OpenAI Gym CARLA',
    project_urls={
        'Source': 'https://github.com/Morphlng/MACarla-Gym',
        'Report bug': 'https://github.com/Morphlng/MACarla-Gym/issues',
        'Author website': 'https://github.com/Morphlng'
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers', 'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ])
