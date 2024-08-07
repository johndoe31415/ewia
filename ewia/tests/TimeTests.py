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

import datetime
from ewia import Time, Observer

class TimeTests(unittest.TestCase):
	def test_timet(self):
		t = Time(datetime.datetime(1970, 1, 1, 0, 0, 0))
		self.assertAlmostEqual(t.timet, 0)

		t = Time(datetime.datetime(1970, 1, 1, 12, 34, 56))
		self.assertAlmostEqual(t.timet, 45296)

		t = Time(datetime.datetime(1970, 1, 1 + 10, 12, 34, 56))
		self.assertAlmostEqual(t.timet, 45296 + (10 * 86400))

	def test_jd(self):
		t = Time(datetime.datetime(2013, 1, 1, 0, 30, 0))
		self.assertAlmostEqual(t.jd, 2456293.520833, places = 6)

	def test_y2000days(self):
		t = Time(datetime.datetime(2000, 1, 2, 12, 0, 0))
		self.assertAlmostEqual(t.days_since_y2000, 1)

		t = Time(datetime.datetime(2000, 1, 3, 13, 0, 0))
		self.assertAlmostEqual(t.days_since_y2000, 2 + (1 / 24))

	def test_local_sidereal_time(self):
		obs = Observer.from_str("N 0", "E 13")
		t = Time(datetime.datetime(2017, 1, 1, 10, 0, 21))
		self.assertAlmostEqual(t.jd, 2457754.91691, places = 6)
		self.assertAlmostEqual(t.local_mean_sidereal_time_hrs(obs), 17 + (37 / 60) + (21 / 3600), places = 3)

		obs = Observer.from_str("N 0", "W 122.49")
		t = Time(datetime.datetime(2010, 1, 2, 20, 34, 5))
		self.assertAlmostEqual(t.jd, 2455199.357, places = 5)
		self.assertAlmostEqual(t.local_mean_sidereal_time_hrs(obs), 19 + (13 / 60) + (36 / 3600), places = 3)

	def test_gmst(self):
		# http://www2.arnes.si/~gljsentvid10/sidereal.htm -- there's an error
		# in this document; it first says 280.46061837 in the equation for
		# GMST, but later in the example uses 281.46061837. Don't have the
		# original (Meeus formula 11.4) available, but other sources also use
		# 280.xxx.
		t = Time.from_str("1994-06-16 18:00:00Z")
		gmst = t.greenwich_mean_sidereal_time_deg
		self.assertAlmostEqual(gmst, 174.771113474402, places = 5)
