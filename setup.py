from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
   name='simba',
   version='1.0',
   description='A clojure-like interpreted language interoperable with Python.',
   license='MIT',
   long_description=long_description,
   author='Jérémie Vaney',
   author_email='jeremievaney@gmail.com',
   packages=['simba'], # would be the same as name
   install_requires=['wheel', 'bar', 'greek'], #external packages acting as dependencies
)
