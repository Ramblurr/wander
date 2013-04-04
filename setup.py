from setuptools import setup, find_packages

setup(name='wander',
    version='1.0',
    description='Wander free',
    author='Casey Link',
    author_email='unnamedrambler@gmail.com',
    url='http://www.python.org/sigs/distutils-sig/',
    scripts=[
        'bin/wander-web',
        'bin/wander-db',
        'bin/wander-cartosync',
        'bin/wander-spotfetch',
    ],
    packages=find_packages(),

    install_requires=[
        'Flask>=0.8',
        'flask-restful',
        'flask-sqlalchemy',
        'sqlalchemy-migrate',
        'cartodb',
        'spot-persist',
    ],

    dependency_links=[
        'https://github.com/Ramblurr/spot-persist/tarball/master#egg=spot-persist',
        'https://github.com/Vizzuality/cartodb-python/tarball/master#egg=cartodb',
    ],
)
