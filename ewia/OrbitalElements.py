#   ewia - A library to calculate astrophysical object positions
#   Copyright (C) 2017-2024 Johannes Bauer
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

import math
from ewia.VectorR3 import VectorR3
from ewia.EquatorialCoordObject import EquatorialCoordObject

class OrbitalElements():
	_EARTH = None

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
			raise Exception("Orbital element \"i\" (inclination, given in degrees) missing.")
		if "Omega" not in data:
			raise Exception("Orbital element \"Omega\" (longitude of the ascending node, given in degrees) missing.")
		if "omega" not in data:
			raise Exception("Orbital element \"omega\" (argument of the periapsis, given in degrees) missing.")
		if "T" not in data:
			raise Exception("Orbital element \"T\" (time of the perihelion passage, given as Julian Date) missing.")
		if "M" not in data:
			raise Exception("Orbital element \"M\" (object mass, given in solar masses) missing.")
		return cls(a = data["a"], e = data["e"], i = data["i"], Omega = data["Omega"], omega = data["omega"], T = data["T"], M = data["M"])

	# Calculates eccentric anomaly using Danby's method
	def __calculate_eccentric_anomaly(self, mean_anomaly):
		u1 = mean_anomaly
		while True:
			u0 = u1
			f0 = u0 - self.e * math.sin(u0) - mean_anomaly
			f1 = 1 - self.e * math.cos(u0)
			f2 = self.e * math.sin(u0)
			f3 = self.e * math.cos(u0)
			d1 = -f0 / f1
			d2 = -f0 / (f1 + d1 * f2 / 2)
			d3 = -f0 / (f1 + (d1 * f2 / 2) + (d2 ** 2) * f3 / 6)
			u1 = u0 + d3
			if abs(u1 - u0) < 1e-15:
				break
		u = u1
		return u

	def __orbital_vectors_at_julian_date(self, t):
		# Orbital period
		P_x = 365.256898326 * (self.a ** 1.5) / (1 + self.M)

		# Mean anomaly
		m_x = (2 * math.pi * (t - self.T) / P_x) % (2 * math.pi)

		# Find the eccentric anomaly
		u_x = self.__calculate_eccentric_anomaly(mean_anomaly = m_x)

		# Find CHPV''' (canonical heliocentric position vector, triple prime)
		chpv3_x = VectorR3(self.a * (math.cos(u_x) - self.e),
							self.a * math.sin(u_x) * math.sqrt(1 - self.e ** 2),
							0)

		# Rotate the triple-prime position vector by the argument of the selfrihelion, ω
		chpv2_x = chpv3_x.rotate_xy(self.omega)

		# Rotate the double-prime position vector by the inclination, i.
		chpv1_x = chpv2_x.rotate_yz(self.i)

		# Rotate the single-prime position vector by the longitude of the ascending node, Ω.
		chpv_x = chpv1_x.rotate_xy(self.Omega)

		return {
			"P":		P_x,		# Orbital period
			"m":		m_x,		# Mean anomaly
			"u":		u_x,		# Eccentric anomaly
			"chpv":		chpv_x,		# CHPV
			"chpv1":	chpv1_x,	# CHPV'
			"chpv2":	chpv2_x,	# CHPV''
			"chpv3":	chpv3_x,	# CHPV'''
		}

	@classmethod
	def calculate_earth_obliquity_deg(cls, obstime):
		# Formula from JPL's Astonomical Almanac for 2010, returns epsilon
		T = obstime.jcent_since_y2000
		epsilon = (23 + (26 / 60) + (21.406 / 3600)) + (1 / 3600) * (
			-46.836769 * T
			- 0.0001831 * (T ** 2)
			+ 0.00200340 * (T ** 3)
			- 5.76e-7 * (T ** 4)
			- 4.34e-8 * (T ** 5)
		)
		return epsilon

	def calculate_equatorial_position(self, observer, obstime):
		# Calculations for object
		res_e = self._EARTH.__orbital_vectors_at_julian_date(obstime.jd)
		res_x = self.__orbital_vectors_at_julian_date(obstime.jd)

		# Find the vector difference between the heliocentric position vector of object X and
		# the heliocentric position vector to Earth.
		d = res_x["chpv"] - res_e["chpv"]

		# Find the current obliquity of Earth and convert to rad.
		epsilon = self.calculate_earth_obliquity_deg(obstime) / 180 * math.pi

		d1 = d.rotate_yz(epsilon)

		distance = d1.length

		right_ascension_rad = math.atan2(d1.y, d1.x)
		right_ascension_hrs = (right_ascension_rad * 24 / (2 * math.pi)) % 24

		declination_deg = math.asin(d1.z / distance) * 180 / math.pi
		equatorial_pos = EquatorialCoordObject(right_ascension_hrs, declination_deg)
		return equatorial_pos

	def calculate_apparent_position(self, observer, obstime):
		equatorial_pos = self.calculate_equatorial_position(observer, obstime)
		return equatorial_pos.calculate_apparent_position(observer, obstime)

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

OrbitalElements._EARTH = OrbitalElements(
	a = 1.00000011,
	e = 0.01671022,
	i = 0.00000087,
	Omega = -0.19653524,
	omega = 1.99330267,
	T = 2454836.125,
	M =	3.003468905535e-06
)
