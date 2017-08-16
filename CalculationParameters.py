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

from DATE import DATE
from SkyPos import SkyPos
from Ephemeris import Ephemeris
from Observer import Observer

class CalculationParameters():
	def __init__(self, options):
		self.__options = options
		self.__data = {
			"localdate":	None,
			"object":		None,
			"localpos":		None
		}

		if self.__options["time"] is None:
			self.__data["localdate"] = DATE("now")
		else:
			self.__data["localdate"] = DATE(self.__options["time"], self.__options["timezone"])

		if self.__options["ephemeris"] is True:
			self.__data["object"] = Ephemeris.calculate(self.__options["object"], self.__data["localdate"])
		else:
			self.__data["object"] = SkyPos(self.__options["object"][0], self.__options["object"][1])

		self.__data["localpos"] = Observer(self.__options["location"][0], self.__options["location"][1])

	def recalculate_skypos(self, newdate):
		if not self.__options["ephemeris"]:
			return
		self.__data["object"] = Ephemeris.calculate(self.__options["object"], newdate)
		return self.__data["object"]

	def __getitem__(self, key):
		return self.__data[key]
