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

class OrbitalElements(object):
	def __init__(self, a, e, i, Omega, omega, T, M):
		self.__a = a
		self.__e = e
		self.__i = i
		self.__Omega = Omega
		self.__omega = omega
		self.__T = T
		self.__M = M

	@property
	def a(self):
		return self.__a

	@property
	def e(self):
		return self.__e

	@property
	def i(self):
		return self.__i

	@property
	def Omega(self):
		return self.__Omega

	@property
	def omega(self):
		return self.__omega

	@property
	def T(self):
		return self.__T

	@property
	def M(self):
		return self.__M

	@classmethod
	def from_data(cls, data):
		if "a" not in data:
			raise Exception("Orbital element \"a\" (semimajor axis, given in AU) missing.")
		if "e" not in data:
			raise Exception("Orbital element \"e\" (ellipse eccentricity) missing.")
		if "i" not in data:
			raise Exception("Orbital element \"i\" (inclination, given in TODO) missing.")
		if "Omega" not in data:
			raise Exception("Orbital element \"Omega\" (longitude of the ascending node) missing.")
		if "omega" not in data:
			raise Exception("Orbital element \"omega\" (argument of the periapsis) missing.")
		if "T" not in data:
			raise Exception("Orbital element \"T\" (epoch, given as Julian Day) missing.")
		if "M" not in data:
			raise Exception("Orbital element \"M\" (object mass, given in solar masses) missing.")
		return cls(a = data["a"], e = data["e"], i = data["i"], Omega = data["Omega"], omega = data["omega"], T = data["T"], M = data["M"])

	def __str__(self):
		elements = [
				("a", self.a),
				("e", self.e),
				("i", self.i),
				("Omega", self.Omega),
				("omega", self.omega),
				("T", self.T),
				("M", self.M),
		]
		elements = ", ".join("%s = %.2e" % (key, value) for (key, value) in elements)
		return "OrbitalElements<%s>" % (elements)

