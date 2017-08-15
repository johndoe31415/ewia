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
#   Johannes Bauer <JohannesBauer@gmx.de>

import re

class EarthPos(object):
	# (?P<deg_float>\d+(\.\d*)?)\s*°?
	# (?P<deg_int>\d+)\s*°(\s*(?P<min_int>\d+)\s*'(\s*(?P<sec_float>\d+(\.\d*)?)\s*'')?)?
	_lat_long_re = re.compile(r"(?P<sign>[NSEW])\s*((?P<deg_float>\d+(\.\d*)?)\s*°?|(?P<deg_int>\d+)\s*°(\s*(?P<min_int>\d+)\s*'(\s*(?P<sec_float>\d+(\.\d*)?)\s*(''|\"))?)?)")

	def __init__(self, latitude, longitude):
		assert(isinstance(latitude, float))
		assert(isinstance(longitude, float))
		assert(-180 < latitude <= 180)
		assert(-90 < longitude <= 90)
		self.__latitude = latitude
		self.__longitude = longitude

	@property
	def latitude(self):
		return self.__latitude

	@property
	def longitude(self):
		return self.__longitude

	@staticmethod
	def __value_to_str_dms_fract(value):
		seconds = round(value * 3600000)
		return "%d°%d′%d.%03d″" % (seconds // 3600000, seconds % 3600000 // 60000, seconds % 3600000 % 60000 // 1000, seconds % 3600000 % 60000 % 1000)

	@staticmethod
	def __value_to_str_dms(value):
		seconds = round(value * 3600)
		return "%d°%d′%d″" % (seconds // 3600, seconds % 3600 // 60, seconds % 3600 % 60)

	@property
	def latitude_str_dms(self):
		return "SN"[self.__latitude > 0] + self.__value_to_str_dms(abs(self.__latitude))

	@property
	def longitude_str_dms(self):
		return "WE"[self.__longitude > 0] + " " + self.__value_to_str_dms(abs(self.__longitude))

	@classmethod
	def latlong_from_string(cls, text, parse_as_latitude = True):
		result = cls._lat_long_re.fullmatch(text)
		if result is None:
			raise Exception("Cannot parse '%s' as %s." % (text, ["longitude", "latitude"][parse_as_latitude]))

		result = result.groupdict()
		if parse_as_latitude and (result["sign"] not in "NS"):
			raise Exception("Cannot parse '%s' as %s: Expected N or S, but got %s." % (text, ["longitude", "latitude"][parse_as_latitude], result["sign"]))
		elif (not parse_as_latitude) and (result["sign"] not in "WE"):
			raise Exception("Cannot parse '%s' as %s: Expected E or W, but got %s." % (text, ["longitude", "latitude"][parse_as_latitude], result["sign"]))

		if result["deg_float"] is not None:
			fresult = float(result["deg_float"])
		else:
			fresult = float(result["deg_int"])
			if result["min_int"] is not None:
				fresult += float(result["min_int"]) / 60
			if result["sec_float"] is not None:
				fresult += float(result["sec_float"]) / 3600
		if result["sign"] in "WS":
			fresult = -fresult
		return fresult

	@classmethod
	def latitude_from_string(cls, text):
		return cls.latlong_from_string(text, parse_as_latitude = True)

	@classmethod
	def longitude_from_string(cls, text):
		return cls.latlong_from_string(text, parse_as_latitude = False)

	@classmethod
	def from_str(cls, latitude_str, longitude_str):
		latitude = cls.latitude_from_string(latitude_str)
		longitude = cls.longitude_from_string(longitude_str)
		return cls(latitude = latitude, longitude = longitude)

	@classmethod
	def from_data(cls, data):
		return cls.from_str(data["latitude"], data["longitude"])

	def __str__(self):
		return "%s, %s" % (self.latitude_str_dms, self.longitude_str_dms)

if __name__ == "__main__":
	#x = EarthPos.from_str("N 1° 2' 3.456''", "E12")
	x = EarthPos.from_str("N 1° 2' 3.456''", "E0")
	print(x)