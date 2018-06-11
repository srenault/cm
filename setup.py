try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='simple-bank-api',
    version='0.0.1',
    author='Maxime Falaize',
    author_email='pro@maxime-falaize.fr',
    packages=['simplebank', ],
    license='GPLv3',
    url='https://github.com/mfalaize/simple-bank-api',
    description='This is a lightweight python 3 API designed to extract data from banks',
    long_description=readme,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
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
