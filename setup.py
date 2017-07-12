from setuptools import setup, find_packages

long_description = """
Asynchronous Http Client written in httptools and asyncio.
The API tries to be like legendery requests.
"""

setup(
    name='asyncrequests',
    version='0.1.0',

    description='Asynchronous Http Client for asyncio',
    long_description=long_description,

    url='https://github.com/RevengeComing/asyncrequests',
    author='Sepehr Hamzelooy',
    author_email='s.hamzelooy@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
    ],
    install_requires=['httptools'],
    packages=find_packages(),

    keywords='requests http client',
)