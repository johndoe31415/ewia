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

import re
import math
from ewia.Tools import ParseTools, MathTools, FormatTools
from ewia.Observer import Observer
from ewia.Time import Time
from ewia.ApparentPosition import ApparentPosition

class EquatorialCoordObject():
	def __init__(self, ra, dec):
		assert(isinstance(ra, float))
		assert(isinstance(dec, float))
		assert(0 <= ra < 24)
		assert(-90 < dec < 90)
		self.__ra = ra
		self.__dec = dec

	@property
	def ra(self):
		return self.__ra

	@property
	def ra_deg(self):
		return self.ra * 15

	@property
	def dec(self):
		return self.__dec

	@property
	def ra_str(self):
		return FormatTools.format_hms(self.__ra)

	@property
	def dec_str(self):
		return FormatTools.format_deg(self.__dec)

	@classmethod
	def from_str(cls, ra_str, dec_str):
		return cls(ra = ParseTools.parse_hms(ra_str), dec = ParseTools.parse_deg(("-", ), ("+", ""), dec_str))

	@classmethod
	def from_data(cls, data):
		return cls.from_str(data["ra"], data["dec"])

	def calculate_apparent_position(self, observer, obstime):
		assert(isinstance(observer, Observer))
		assert(isinstance(obstime, Time))
		lst_deg = obstime.local_mean_sidereal_time_deg(observer)
		hour_angle_deg = lst_deg - self.ra_deg

		(dsin, dcos) = (MathTools.dsin, MathTools.dcos)

		A = (dsin(self.dec) * dsin(observer.latitude)) + (dcos(self.dec) * dcos(observer.latitude) * dcos(hour_angle_deg))
		altitude = math.asin(A) * 180 / math.pi

		B = (dsin(self.dec) - (dsin(altitude) * dsin(observer.latitude))) / (dcos(altitude) * dcos(observer.latitude))
		azimuth = math.acos(B) * 180 / math.pi
		if dsin(hour_angle_deg) >= 0:
			azimuth = (-azimuth) % 360

		return ApparentPosition(altitude = altitude, azimuth = azimuth, observed_object = self, observer_location = observer, observation_time = obstime)

	def __str__(self):
		return "EquatorialCoordObject<RA = %s, DEC = %s>" % (self.ra_str, self.dec_str)
