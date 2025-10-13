from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='orcas-cli',
    version='0.1.0',
    author='Eric Moghioros',
    author_email='eric.moghioros000@gmail.com',
    description='Transform natural language into safe bash commands using local model',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Mogalina/orcas',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    python_requires='>=3.8',
    install_requires=[
        'llama-cpp-python>=0.2.0',
        'pyyaml>=6.0',
        'click>=8.0.0',
        'colorama>=0.4.6',
        'prompt-toolkit>=3.0.0',
        'rich>=13.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'orcas=cli:main',
        ],
    },
    include_package_data=True,
)