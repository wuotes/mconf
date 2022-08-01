from setuptools import setup

def read_file(filename: str) -> str:
    text_result = r''

    with open(filename, r'r') as the_file:
        text_result = the_file.read()

    return text_result

setup(
    name=r'mconf',
    version=r'1.0.0',    
    description=r'Manage multiple TOML configurations from a single module.',
    long_description=read_file(r'./README.md'),
    long_description_content_type=r'text/markdown',
    url=r'https://github.com/wuotes/mconf',
    download_url=r'https://pypi.org/project/mconf/',
    author=r'Jordan Schaffrin',
    author_email=r'mailbox@xrtuen.com',
    license=r'Mozilla Public License 2.0',
    python_requires=r'>=3.9',
    packages=[r'mconf'],
    install_requires=[r'tomli>=2.0.1',
                      r'tomli_w>=1.0.0',                     
                      ],

    classifiers=[
        r'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        r'Programming Language :: Python :: 3.9',
        r'Programming Language :: Python :: 3.10',
        r'Programming Language :: Python :: 3.11',
        r'Programming Language :: Python :: 3.12',
        r'Operating System :: Microsoft :: Windows',
        r'Operating System :: POSIX :: Linux',
        r'Operating System :: MacOS',
    ],
)
