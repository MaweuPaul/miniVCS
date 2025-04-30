from setuptools import setup ,find_packages

setup(
    name="minivcs",
    version="0.1",
    packages=find_packages(),
    scripts=["minivcs"],
        entry_points={
        'console_scripts': [
            'minivcs=minivcs.main:main',
        ],
    },
    author="Paul Maweu",
    author_email="paulmaweu.pm@gmail.com",
    description="A lightweight version control system inspired by Git",
    keywords="vcs, git, version control",
    url="https://github.com/MaweuPaul/miniVCS",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Version Control",
    ],
)