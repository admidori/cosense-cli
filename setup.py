from setuptools import setup
setup(
    name="cosense",
    version="0.1.0",
    author="Aoi Kondo",
    author_email="agotadmidori@gmail.com",
    description="The CLI reader for cosense",
    license="MIT",
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "cosense = cosense.cli.main:main",
        ]
    },
)
