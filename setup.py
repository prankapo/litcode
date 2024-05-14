from setuptools import setup, find_packages

version = '0.10'

setup(
	name = 'litcode',
	version = version,
	packages = ['litcode'],
	entry_points = {
		'console_scripts' : [
			'linit=litcode.linit:main',
			'ltangle=litcode.ltangle:main',
			'lweave=litcode.lweave:main'
		]
	}
)

