from setuptools import setup, find_packages

setup(
    name="Horus-RPi5",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "opencv-python",
        "pyserial",
        "wxPython",
        "Pillow"
    ],
)
