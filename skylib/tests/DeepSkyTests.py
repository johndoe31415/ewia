#   Ewia - A tool to calculate astrophysical object positions.
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

from skylib import DeepSkyObject, Observer, Time

class DeepSkyTests(unittest.TestCase):
	def test_deepsky1(self):
		# http://www.convertalot.com/celestial_horizon_co-ordinates_calculator.html
		observer = Observer.from_str("N 42° 21'", "W 71° 4'")
		obstime = Time.from_str("2004-04-06 19:00:00Z")
		dsobject = DeepSkyObject.from_str("03:47", "+24° 7'")
		apparent = dsobject.calculate_apparent_position(observer, obstime)
		self.assertAlmostEqual(apparent.altitude, 70.76031714756199, places = 2)
		self.assertAlmostEqual(apparent.azimuth, 159.05385342558554, places = 2)

	def test_deepsky2(self):
		# http://www.stargazing.net/kepler/altaz.html
		observer = Observer.from_str("N 52° 30'", "W 1° 55'")
		obstime = Time.from_str("1998-08-10 23:10:00Z")
		dsobject = DeepSkyObject.from_str("16:41.7", "36° 28'")

		self.assertAlmostEqual(dsobject.ra, 16.695)
		self.assertAlmostEqual(dsobject.dec, 36.466667, places = 6)
		self.assertAlmostEqual(obstime.time, 23.166667, places = 6)
		self.assertAlmostEqual(observer.latitude, 52.5)
		self.assertAlmostEqual(observer.longitude, -1.9166667)

		lst_deg = obstime.local_siderial_time_deg(observer)
		self.assertAlmostEqual(lst_deg, 304.80761)

		apparent = dsobject.calculate_apparent_position(observer, obstime)
		self.assertAlmostEqual(apparent.altitude, 49.169122, places = 4)
		self.assertAlmostEqual(apparent.azimuth, 269.14634, places = 4)
