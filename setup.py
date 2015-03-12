from distutils.core import setup

setup(
    name='ig_markets',
    version='0.1',
    packages=['ig_markets'],
    install_requires=['pyaml',
                      'requests',
                      'certifi',
                      'pandas'],
    url='https://github.com/ericgarrigues/ig_markets.git',
    license='BSD',
    author='Eric Garrigues',
    author_email='eric@automata.io',
    description='IG Markets Stream and REST clients.',
    long_description="""IG markets Stream and REST clients. Based on Lewis Barber
    (https://github.com/lewisbarber/ig-markets-rest-api-python-library) and femtodrader
    (https://github.com/femtotrader/ig-markets-stream-api-python-library) works.
    """
)
