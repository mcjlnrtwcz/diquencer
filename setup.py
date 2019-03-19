import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="diquencer",
    version="0.4.0",
    author="Maciej Lenartowicz",
    author_email="mcjlnrtwcz@gmail.com",
    description="Simple MIDI sequencer library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mcjlnrtwcz/diquencer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["python-rtmidi~=1.2.1"],
)
