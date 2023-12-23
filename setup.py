from setuptools import setup, find_packages


setup(
    name = 'litcode',
    version = '0.1.0',

    packages = find_packages(),

    entry_points = {
        'console_scripts' : [
            'linit=litcode.linit:main',
            'ldump=litcode.ldump:main',
            'ltangle=litcode.ltangle:main',
            'lweave=litcode.lweave:main'
        ]
    }
)


