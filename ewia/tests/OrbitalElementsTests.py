#   ewia - A library to calculate astrophysical object positions
#   Copyright (C) 2017-2017 Johannes Bauer
#
#   This file is part of Ewia.
#
#    Ewia is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; this program is ONLY licensed under
#    version 2 of the License, later versions are explicitly excluded.
#
#    Ewia is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Ewia; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#   Johannes Bauer <JohannesBauer@gmx.de>

import unittest

from ewia import OrbitalElements, Observer, Time

class OrbitalElementsTests(unittest.TestCase):
	@staticmethod
	def _jupiter():
		return OrbitalElements.from_data({
			"a":		5.20336301,
			"e":		0.04839266,
			"i":		0.02278178,
			"Omega":	1.75503590,
			"omega":	4.78565267,
			"T":		2451305.445,
			"M":		9.545523100900e-04
		})

	def test_jupiter(self):
		observer = Observer.from_str("N 48° 51' 12.27\"", "E 2° 20' 55.68\"")
		obstime = Time.from_localtime_str("2017-08-16 20:00:53", "Europe/Paris")

		jupiter = self._jupiter()
		equatorial = jupiter.calculate_equatorial_position(observer, obstime)
		self.assertAlmostEqual(equatorial.ra, 13 + (13 / 60) + (12.22 / 3600), places = 2)
		self.assertAlmostEqual(equatorial.dec, -(6 + (31 / 60) + (28.0 / 3600)), places = 1)
		apparent = jupiter.calculate_apparent_position(observer, obstime)
		self.assertAlmostEqual(apparent.azimuth, 224 + (11 / 60) + (15.7 / 3600), places = 0)
		self.assertAlmostEqual(apparent.altitude, 24 + (45 / 60) + (32.5 / 3600), places = 1)

