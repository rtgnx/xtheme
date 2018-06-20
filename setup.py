from setuptools import setup

with open("README.md", "r") as fd:
    long_description = fd.read()

setup(name='xtheme',
    version='0.3',
    description='theme generator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/rtgnx/xtheme',
    author='Adrian Cybulski',
    author_email='adrian@rtgnx.xyz',
    license='GPL2',
    install_requires=['click', 'toml', 'jinja2'],
    packages=['xtheme'],
    entry_points = {
      'console_scripts': ['xtheme=xtheme:main'],
    },
    zip_safe=False,
    classifiers=(
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
      "Operating System :: POSIX :: Linux"
    ))
