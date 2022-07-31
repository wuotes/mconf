from setuptools import setup

import codecs
import os.path

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))

    with codecs.open(os.path.join(here, rel_path), r'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith(r'__version__'):
            delim = r'"' if r'"' in line else r"'"

            return line.split(delim)[1]

    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name='mconf',
    version=get_version("mconf/__init__.py"),    
    description='Manage multiple TOML configurations from a single module.',
    url='https://github.com/wuotes/mconf',
    author='Jordan Schaffrin',
    author_email='mailbox@xrtuen.com',
    license='Mozilla Public License 2.0',
    packages=['mconf'],
    install_requires=['tomli>=2.0.1',
                      'tomli_w>=1.0.0',                     
                      ],

    classifiers=[
        'License :: OSI Approved :: MPL-2.0 License',
        'Programming Language :: Python :: 3.9',
    ],
)
