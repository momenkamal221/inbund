from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='my_library',
    version='1.0.0',
    author='Your Name',
    author_email='your@email.com',
    description='A short description of your library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_library',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)