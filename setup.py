from setuptools import find_packages, setup

with open("./README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="delogger",
    version="0.2.4",
    description="delogger is a convenient logging package",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="deresmos",
    author_email="deresmos@gmail.com",
    url="https://github.com/deresmos/delogger",
    python_requires=">=3.4",
    packages=find_packages(),
    include_package_data=False,
    keywords=["logging", "Logger"],
    license="MIT License",
    install_requires=["requests", "colorlog"],
    extras_require={"develop": ["twine", "flake8", "pytest", "pytest-sugar", "black"]},
)
