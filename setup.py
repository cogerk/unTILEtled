from setuptools import setup, find_packages

setup(
    name="example",
    version="0.1.0",
    packages=find_packages(include=["exampleproject", "exampleproject.*"]),
    install_requires=[
        "numpy==1.21.5",
        "pip==22.0.3",
        "pyglet==1.5.21",
        "setuptools==60.6.0",
        "wheel==0.37.1",
        "black==22.1.0",
    ],
    # extras_require={
    #    'interactive': ['matplotlib>=2.2.0,, 'jupyter'],
    # }
    setup_requires=["black"],
)
