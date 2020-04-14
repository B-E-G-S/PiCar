from setuptools import setup, find_packages
setup(name="picar",
      version="0.0.1",
      packages=find_packages(),
      install_requires = [
          "numpy~=1.18.1",
          "pycairo~=1.19.0",
          "PyGObject~=3.34.0",
          "opencv-contrib-python~=4.2.0.32"
      ]
)
