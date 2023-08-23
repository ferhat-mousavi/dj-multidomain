from setuptools import setup, find_packages

setup(
    name='dj-multidomain',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'django',
    ],
    author='Ferhat Mousavi',
    author_email='ferhat.mousavi@gmail.com',
    description='A Django middleware to handle multiple domains.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/ferhat-mousavi/dj-multidomain',
)
