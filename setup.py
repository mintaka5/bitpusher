from setuptools import setup, find_packages

setup(
    name="bitpusher",
    author="Chris Walsh",
    author_email="chris.is.rad@pm.me",
    classifiers=[],
    description="",
    install_requires=[],
    license="BSD-3 Clause",
    version="0.0.1",
    url="",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bitpusher = datapuller.knowone:boot_up',
            'bitpushi = pushi.gui:boot_up',
            'coda = codex.valuer:init'
        ]
    }
)
