#   Ewia - A tool to calculate astrophysical object positions.
#   Copyright (C) 2009-2017 Johannes Bauer
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

class VectorR3(object):
	def __init__(self, x, y, z):
		self.__x = x
		self.__y = y
		self.__z = z

	@property
	def x(self):
		return self.__x

	@property
	def y(self):
		return self.__y

	@property
	def z(self):
		return self.__z

	@property
	def length(self):
		return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

	def rotate_xy(self, phi):
		"""Rotate a vector around the the normal vector of the XY plane (Z axis)
		angle phi, given in radians."""
		return VectorR3(
			self.x * cos(phi) - self.y * sin(phi),
			self.x * sin(phi) + self.y * cos(phi),
			self.z
		)

	def rotate_yz(self, phi):
		"""Rotate a vector around the the normal vector of the YZ plane (X
		axis) angle phi, given in radians."""
		return VectorR3(
			self.x,
			self.y * cos(phi) - self.z * sin(phi),
			self.y * sin(phi) + self.z * cos(phi)
		)

	def __add__(self, other):
		return VectorR3(self.x + other.x,
						self.y + other.y,
						self.z + other.z)

	def __sub__(self, other):
		return VectorR3(self.x - other.x,
						self.y - other.y,
						self.z - other.z)

	def __repr__(self):
		return "VecR3<%s>" % (str(self))

	def __str__(self):
		return "{ %.4f, %.4f, %.4f }" % (self.x, self.y, self.z)

