#   ewia - A library to calculate astrophysical object positions
#   Copyright (C) 2009-2024 Johannes Bauer
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
from ewia.Tools import ParseTools, FormatTools

class Observer():
	def __init__(self, latitude: float, longitude: float, timezone = None):
		assert(isinstance(latitude, float))
		assert(isinstance(longitude, float))
		assert(-90 < latitude <= 90)
		assert(-180 < longitude <= 180)
		self.__latitude = latitude
		self.__longitude = longitude
		self.__timezone = timezone

	def json(self):
		result = {
			"lat":	self.latitude,
			"lon":	self.longitude,
		}
		if self.__timezone is not None:
			result["tz"] = self.__timezone
		return result

	@property
	def latitude(self):
		return self.__latitude

	@property
	def longitude(self):
		return self.__longitude

	@property
	def timezone(self):
		return self.__timezone

	@property
	def latitude_str_dms(self):
		return FormatTools.format_deg(self.latitude, "S", "N")

	@property
	def longitude_str_dms(self):
		return FormatTools.format_deg(self.longitude, "W", "E")

	@classmethod
	def latitude_from_string(cls, text):
		return ParseTools.parse_deg(("S", ), ("N", ), text)

	@classmethod
	def longitude_from_string(cls, text):
		return ParseTools.parse_deg(("W", ), ("E", ), text)

	@classmethod
	def from_str(cls, latitude_str, longitude_str, timezone = None):
		latitude = cls.latitude_from_string(latitude_str)
		longitude = cls.longitude_from_string(longitude_str)
		return cls(latitude = latitude, longitude = longitude, timezone = timezone)

	@classmethod
	def from_data(cls, data):
		return cls.from_str(data["latitude"], data["longitude"], timezone = data.get("timezone"))

	def __str__(self):
		return "%s, %s" % (self.latitude_str_dms, self.longitude_str_dms)

if __name__ == "__main__":
	#x = Observer.from_str("N 1° 2' 3.456''", "E12")
	x = Observer.from_str("N 1° 2' 3.456''", "E0")
	print(x)
