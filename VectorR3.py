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

from math import sqrt, sin, cos
class VectorR3():
	def __init__(self, x, y, z):
		self.__vals = [ x, y, z ]

	def __sub__(self, other):
		return VectorR3(self.__vals[0] - other.__vals[0],
						self.__vals[1] - other.__vals[1],
						self.__vals[2] - other.__vals[2])

	def __getitem__(self, idx):
		return self.__vals[idx]

	def __str__(self):
		return "{ %.4f %.4f %.4f }" % (self.__vals[0], self.__vals[1], self.__vals[2])

	def __repr__(self):
		return "VecR3 %s" % (str(self))

	def length(self):
		return sqrt(self.__vals[0] ** 2 + self.__vals[1] ** 2 + self.__vals[2] ** 2)

	# Rotate a vector around the the normal vector of the XY plane (Z axis)
	def rotate_xy(self, phi):
		return VectorR3(
			self.__vals[0] * cos(phi) - self.__vals[1] * sin(phi),
			self.__vals[0] * sin(phi) + self.__vals[1] * cos(phi),
			self.__vals[2]
		)

	# Rotate a vector around the the normal vector of the YZ plane (X axis)
	def rotate_yz(self, phi):
		return VectorR3(
			self.__vals[0],
			self.__vals[1] * cos(phi) - self.__vals[2] * sin(phi),
			self.__vals[1] * sin(phi) + self.__vals[2] * cos(phi)
		)

