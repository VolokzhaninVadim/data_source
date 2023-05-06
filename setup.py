from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='data_source',
    version='1.1.1',
    description='Interaction with data source',
    url='https://github.com/VolokzhaninVadim/data_source',
    author='Volokzhanin Vadim',
    author_email='volokzhanin@yandex.ru',
    license='Volokzhanin Vadim',
    include_package_data=True,
    packages=find_packages(),
    install_requires=requirements,
    zip_safe=False
)
