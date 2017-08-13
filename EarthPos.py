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

class EarthPos(object):
	def __init__(self, latitude, longitude):
		if latitude[0] not in [ "N", "S" ]:
			raise Exception("Local earth position latitude must start with N or S")
		if longitude[0] not in [ "W", "E" ]:
			raise Exception("Local earth position latitude must start with W or E")

		self.__latitude = DEG(latitude[1:])
		self.__longitude = DEG(longitude[1:])

		if latitude[0] == "S":
			self.__latitude.negate()

		if longitude[0] == "W":
			self.__longitude.negate()

	def latitude(self):
		return self.__latitude

	def longitude(self):
		return self.__longitude

	def __str__(self):
		return "%s%s, %s%s" % (["S", "N"][self.__latitude >= 0], str(self.__latitude), ["W", "E"][self.__longitude >= 0], str(self.__longitude))
