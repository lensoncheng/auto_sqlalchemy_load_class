from setuptools import setup, find_packages

requires=[]

try:
    import sqlalchemy
except Exception, e:
    requires.append( 'sqlalchemy' )

setup(
        name='autoload',
        version='0.1',
        description='auto create mapper class with database tables',
        packages = find_packages(),
        zip_safe=False,
        install_packages_data=True,
        install_requires=requires,
)
