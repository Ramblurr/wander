from setuptools import setup, find_packages

setup(name='wander',
    version='1.0.1',
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
        'flask-restful>=0.1.7',
        'flask-admin',
        'flask-sqlalchemy>=0.16',
        'flask-login',
        'flask-openid',
        'flask-bootstrap',
        'sqlalchemy==0.7.9',
        'sqlalchemy-migrate==0.7.2',
        'cartodb',
        'spot-persist',
        'apscheduler',
    ],

    dependency_links=[
        'https://github.com/Ramblurr/spot-persist/tarball/master#egg=spot-persist',
        'https://github.com/Vizzuality/cartodb-python/tarball/master#egg=cartodb',
    ],
)
