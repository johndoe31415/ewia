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

import re
from skylib.Tools import ParseTools

class DeepSkyPos(object):
	def __init__(self, ra, dec):
		assert(isinstance(ra, float))
		assert(isinstance(dec, float))
		assert(0 <= ra < 24)
		assert(-90 < dec < 90)
		self.__ra = ra
		self.__dec = dec
		print(self)

	@property
	def ra(self):
		return self.__ra

	@property
	def dec(self):
		return self.__dec

	@classmethod
	def from_data(cls, data):
		return cls(ra = ParseTools.parse_hms(data["ra"]), dec = ParseTools.parse_deg(("-", ), ("+", ""), data["dec"]))

	def __str__(self):
		return "DeepSkyPos<RA = %.3f hrs, dec = %.3f°>" % (self.ra, self.dec)
