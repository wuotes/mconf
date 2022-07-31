from setuptools import setup

setup(
    name='mconf',
    version='1.0.0',    
    description='Manage multiple TOML configurations from a single module.',
    url='https://github.com/wuotes/mconf',
    author='Jordan Schaffrin',
    author_email='mailbox@xrtuen.com',
    license='Mozilla Public License 2.0',
    python_requires='>=3.9'
    packages=['mconf'],
    install_requires=['tomli>=2.0.1',
                      'tomli_w>=1.0.0',                     
                      ],

    classifiers=[
        'License :: OSI Approved :: MPL-2.0 License',
        'Programming Language :: Python :: 3.9',
    ],
)
