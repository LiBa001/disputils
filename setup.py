from setuptools import setup, find_packages

with open("README.rst", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="disputils",
    version="0.2.1",
    description="Some utilities for discord.py. Making Discord bot development easier.",
    long_description=readme,
    long_description_content_type="text/x-rst",
    url="https://github.com/LiBa001/disputils",
    author="Linus Bartsch",
    author_email="linus.pypi@mabasoft.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    python_requires=">=3.6",
    install_requires=["discord.py @ git+https://github.com/Rapptz/discord.py@master"],
    keywords="discord discord-py discord-bot utils utility",
    packages=find_packages(exclude=["examples", "docs", "tests"]),
    data_files=None,
)
