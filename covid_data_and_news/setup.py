import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="covid_data_and_news_pkg_scourt",
    version="0.0.1",
    author="Stefan Court",
    author_email="sc1136@exeter.ac.uk",
    description="Returns up to date covid data and news when scheduled",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scourt/covid_data_and_news",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)