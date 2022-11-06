from setuptools import setup

setup(
    name='dali',
    version='0.0.5',
    py_modules=['dali'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'dali = dali:cli',
        ],
    },
)