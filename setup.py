from setuptools import setup

setup(name='xtheme',
    version='0.1',
    description='theme generator',
    url='http://github.com/rtgnx/xtheme',
    author='Adrian Cybulski',
    author_email='adrian@rtgnx.xyz',
    license='GPL2',
    install_requires=['click', 'toml', 'jinja2'],
    packages=['xtheme'],
    entry_points = {
      'console_scripts': ['xtheme=xtheme:main'],
    },
    zip_safe=False)
