try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='sre-cm',
    version='0.0.1',
    author='Sebastien Renault',
    author_email='srenault.contact@gmail.com',
    package_dir = {'': 'lib'},
    packages=['cm', ],
    license='GPLv3',
    url='https://github.com/srenault/cm',
    description='This is a lightweight python 3 API designed to extract data from cm',
    long_description=readme,
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Utilities',
    ],
    install_requires=[
        'requests >= 2.9.0',
        'beautifulsoup4 >= 4.4.0'
    ],
    python_requires='>=3'
)
