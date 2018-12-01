from setuptools import find_packages, setup

setup(
    name='delogger',
    version='0.1.2',
    description='delogger is a convenient logging package',
    author='deresmos',
    author_email='deresmos@gmail.com',
    python_requires='>=3.4',
    packages=find_packages(),
    include_package_data=False,
    keywords=['logging', 'Logger'],
    license='MIT License',
    install_requires=['requests', 'colorlog'],
    extras_require={
        'develop': [
            'twine',
            'flake8',
            'pytest',
            'pytest-sugar',
        ],
    },
)
