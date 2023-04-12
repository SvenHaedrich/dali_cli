from setuptools import setup, find_packages

setup(
    name="dali",
    version="0.0.6",
    py_modules=["dali"],
    install_requires=["click", "pyserial", "pyusb", "termcolor"],
    packages=find_packages(where='dali'),
    package_dir={"":"dali"},
    entry_points={
        "console_scripts": [
            "dali = dali:cli",
        ],
    },
)
