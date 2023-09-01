from setuptools import setup, find_packages

setup(
    name='dj-multidomain',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'django>=4.0',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Framework :: Django',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
    ],
    author='Ferhat Mousavi',
    author_email='ferhat.mousavi@gmail.com',
    description='A Django middleware module to handle multiple domains.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/ferhat-mousavi/dj-multidomain',
)
