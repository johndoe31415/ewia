import setuptools

with open("README.md") as f:
	long_description = f.read()

setuptools.setup(
	name = "ewia",
	packages = setuptools.find_packages(),
	version = "0.0.2",
	license = "gpl-3.0",
	description = "A library to calculate astrophysical object positions",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Johannes Bauer",
	author_email = "joe@johannes-bauer.com",
	url = "https://github.com/johndoe31415/ewia",
	download_url = "https://github.com/johndoe31415/ewia/archive/v0.0.2.tar.gz",
	keywords = [ "astrophysics", "calculator", "position", "deep-sky", "ephemeris", "planets" ],
	install_requires = [
		"pytz",
	],
	entry_points = {
		"console_scripts": [
			"ewia = ewia.__main__:main"
		]
	},
	include_package_data = True,
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.10",
		"Programming Language :: Python :: 3.11",
		"Programming Language :: Python :: 3.10",
	],
)
