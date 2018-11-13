from setuptools import find_packages, setup

__author__ = 'deresmos'

setup(
    name='delogger',
    version='0.0.1',
    description='delogger is a convenient logging package',
    author='deresmos',
    author_email='deresmos@gmail.com',
    packages=find_packages(),
    include_package_data=False,
    keywords=['logging', 'Logger'],
    license='MIT License',
    install_requires=['requests', 'colorlog'],
    extras_require={
        'develop': [
            'flake8',
            'pytest',
            'pytest-sugar',
        ],
    },
)
