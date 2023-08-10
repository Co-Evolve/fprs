from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='fprs',
    version='0.1.0',
    description='A Framework for defining Parameterized Robot Descriptions.',
    long_description=readme,
    url='https://github.com/Co-Evolve/fprs',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=required
)
