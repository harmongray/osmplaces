from setuptools import setup, find_packages

setup(name='osmplaces',
    version='0.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'osmplaces=osmplaces.__main__:main'
            ]
        },
        install_requires=[
            'tqdm',
            'argparse'
                ],
        python_requires='>=3.8',
        description='A tool for parsing place names from osmosis output',
        author='Harmon Grey',
        author_email='greytradecraft@gmail.com'
    )

