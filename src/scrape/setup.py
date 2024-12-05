from setuptools import setup

requirements = [
    "random",
    "time",
    "selenium",
    "subprocess",
    "numpy",
    "pandas",
    "sqlalchemy",
    "matplotlib",
]


requirements_dev = ["black", "flake8", "isort", "pre-commit", "pytest", "pytest-cov"]


setup(
    name="scrape",
    version="0.1.0",
    description="scraping grand tour data and create a database",
    author="deniz",
    url="https://github.com/heineborell/tdf_results.git",
    packages=["scrape"],
    package_dir={"": "src"},
    install_requires=requirements,
    extra_require={"dev": requirements_dev},
)
