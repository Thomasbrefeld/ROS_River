from setuptools import setup

setup(
	version='0.0.0',
	scripts=['src/simple_display_test.py',
		'src/main1.py'],
	packages=['ros_river'],
	package_dir={'' : 'src'}
)
