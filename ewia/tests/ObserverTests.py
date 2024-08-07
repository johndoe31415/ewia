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

from ewia import Observer

class ObserverTests(unittest.TestCase):
	def test_pos1(self):
		pos = Observer.from_str("N 12.3456", "E 12.34")
		self.assertAlmostEqual(pos.latitude, 12.3456)
		self.assertAlmostEqual(pos.longitude, 12.34)

		pos = Observer.from_str("S 12.3456", "E 12.34")
		self.assertAlmostEqual(pos.latitude, -12.3456)
		self.assertAlmostEqual(pos.longitude, 12.34)

		pos = Observer.from_str("S 12.3456", "W 12.34")
		self.assertAlmostEqual(pos.latitude, -12.3456)
		self.assertAlmostEqual(pos.longitude, -12.34)

	def test_pos_deg(self):
		pos = Observer.from_str("N 5° 7' 11.201\"", "E 11° 13' 17.101\"")
