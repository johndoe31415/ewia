#   Ewia - A tool to calculate astrophysical object positions.
#   Copyright (C) 2009-2009 Johannes Bauer
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
#   Johannes Bauer
#   JohannesBauer@gmx.de

from math import sin, cos, asin, acos, pi
from RA import RA
from DEC import DEC
from HMS import HMS
from DEG import DEG
class SkyPos():
	def __init__(self, ra, dec):
		self.__ra = RA(ra)
		self.__dec = DEC(dec)

	def __str__(self):
		return "RA %s, DEC %s" % (str(self.__ra), str(self.__dec))

	def hourangle(self, lst):
		return HMS(lst.value() - self.__ra.value())

	def alt_az(self, lst, earthpos):
		A = sin(self.__dec.rad()) * sin(earthpos.latitude().rad()) + cos(self.__dec.rad()) * cos(earthpos.latitude().rad()) * cos(self.hourangle(lst).dms().rad())
		alt = asin(A)

		B = (sin(self.__dec.rad()) - sin(alt) * sin(earthpos.latitude().rad())) / (cos(alt) * cos(earthpos.latitude().rad()))
		azimuth = acos(B)
		if sin(self.hourangle(lst).dms().rad()) > 0:
			azimuth = (2 * pi) - azimuth

		return (DEG(alt * 180 / pi), DEG(azimuth * 180 / pi))

	def ra(self):
		return self.__ra

	def dec(self):
		return self.__dec
