from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='inbund',
    version='1.0.0',
    author='Your Name',
    author_email='',
    description='A short description of your library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/yourusername/my_library',
    package_data={
        '': ['cli/*','main*'],
    },
    packages=find_packages(exclude=['tests']),  # This will find packages within the 'inbund' directory
    include_package_data=True,
)
