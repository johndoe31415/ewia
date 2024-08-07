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

from ewia import EquatorialCoordObject, Observer, Time

class EquatorialCoordTests(unittest.TestCase):
	def test_deepsky1(self):
		# http://www.convertalot.com/celestial_horizon_co-ordinates_calculator.html
		observer = Observer.from_str("N 42° 21'", "W 71° 4'")
		obstime = Time.from_str("2004-04-06 19:00:00Z")
		dsobject = EquatorialCoordObject.from_str("03:47", "+24° 7'")
		apparent = dsobject.calculate_apparent_position(observer, obstime)
		self.assertAlmostEqual(apparent.altitude, 70.76031714756199, places = 2)
		self.assertAlmostEqual(apparent.azimuth, 159.05385342558554, places = 2)

	def test_deepsky2(self):
		# http://www.stargazing.net/kepler/altaz.html
		observer = Observer.from_str("N 52° 30'", "W 1° 55'")
		obstime = Time.from_str("1998-08-10 23:10:00Z")
		dsobject = EquatorialCoordObject.from_str("16:41.7", "36° 28'")

		self.assertAlmostEqual(dsobject.ra, 16.695)
		self.assertAlmostEqual(dsobject.dec, 36.466667, places = 6)
		self.assertAlmostEqual(obstime.time, 23.166667, places = 6)
		self.assertAlmostEqual(observer.latitude, 52.5)
		self.assertAlmostEqual(observer.longitude, -1.9166667)

		lst_deg = obstime.local_mean_sidereal_time_deg(observer)
		self.assertAlmostEqual(lst_deg, 304.80761, places = 3)

		apparent = dsobject.calculate_apparent_position(observer, obstime)
		self.assertAlmostEqual(apparent.altitude, 49.169122, places = 3)
		self.assertAlmostEqual(apparent.azimuth, 269.14634, places = 3)

	def test_deepsky_stellarium(self):
		observer = Observer.from_str("N 48° 51' 12.27\"", "E 2° 20' 55.68\"")
		obstime = Time.from_localtime_str("2017-08-16 23:25:22", "Europe/Paris")
		dsobject = EquatorialCoordObject.from_str("20:22:00.54", "-14° 43' 20.4\"")		# beta Cap

		apparent = dsobject.calculate_apparent_position(observer, obstime)
		self.assertAlmostEqual(apparent.azimuth, 162 + (32 / 60) + (50.2 / 3600), places = 2)
		self.assertAlmostEqual(apparent.altitude, 24 + (49 / 60) + (28.4 / 3600), places = 1)


