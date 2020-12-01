# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

def get_version():
    version_file = "pexpect_serial_terminal/_version.py"
    with open(version_file) as f:
        exec(compile(f.read(), version_file, "exec"))
    return locals()["__version__"]

setup(
    name='pexpect-serial-terminal',
    version=get_version(),
    author='Johnny Chiang',
    author_email='johnny641119@gmail.com',
    description='serial terminal for pexpect on both windows and linux platforms',
    license='MIT License',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/angryisland/pexpect-serial-terminal',
    packages=find_packages(exclude=('tests', 'docs', 'examples')),
    python_requires=">=3.0",
    install_requires=['pyserial'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)