from setuptools import setup
setup(
    name="cosense",
    version="0.2.0",
    author="Aoi Kondo",
    author_email="agotadmidori@gmail.com",
    description="The CLI reader for cosense",
    license="MIT",
    install_requires=[
        "requests",
        "windows-curses;platform_system=='Windows'",
    ],
    entry_points={
        "console_scripts": [
            "cosense = cosense.cli.main:main",
        ]
    },
)
