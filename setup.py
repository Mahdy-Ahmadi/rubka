from setuptools import setup, find_packages

try:
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''

setup(
    name='Rubka',
    version='4.4.6',
    description='A Python library for interacting with Rubika Bot API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Mahdi Ahmadi',
    author_email='mahdiahmadi.1208@gmail.com',
    maintainer='Mahdi Ahmadi',
    maintainer_email='mahdiahmadi.1208@gmail.com',
    url='https://github.com/Mahdy-Ahmadi/Rubka',
    download_url='https://github.com/Mahdy-Ahmadi/Rubka/archive/refs/tags/v0.1.0.tar.gz',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
)
