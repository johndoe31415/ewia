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

from HMS import HMS
from RE import RE
from DEG import DEG
import time
class DATE():
	def __init__(self, date, timezone = 0.00):	# TZ in hours
		if timezone is None:
			timezone = 0.0

		if date == "now":
			self.__tm = time.time()
			self.__timezone = -time.altzone
			return

		date_re = RE("^([0-9]{4})-([0-9]{2})-([0-9]{2})(.*)")
		if date_re.match(date):
			year = int(date_re[1])
			mon = int(date_re[2])
			day = int(date_re[3])
			self.__tm = time.mktime((year, mon, day, 0, 0, 0, 0, 0, 0)) - time.timezone		# TODO: altzone?
			if date_re[4] is not None:
				self.__tm += HMS(date_re[4]).value() * 3600
		self.__timezone = timezone * 3600
		self.__tm -= self.__timezone
		# Now self.__tm is the time in UT

	def days_since_y2k(self):
		y2k = time.mktime((2000, 1, 1, 12, 0, 0, 0, 0, 0)) - time.timezone		# TODO: altzone?
		days = (self.__tm - y2k) / 86400
		return days

	def tzhrs(self):
		return int(self.__timezone / 3600)

	def tzmin(self):
		return round((abs(self.__timezone) - 3600 * abs(self.tzhrs())) / 60)

	def __str__(self):
		(year, mon, day, hrs, min, sec, x, y, z) = time.gmtime(self.__tm)
		dtstr = "%04d-%02d-%02d %d:%02d:%02d UT" % (year, mon, day, hrs, min, sec)
		return dtstr
	
	def localstr(self):
		(year, mon, day, hrs, min, sec, x, y, z) = time.gmtime(self.__tm + self.__timezone)

		dtstr = "%04d-%02d-%02d %d:%02d:%02d" % (year, mon, day, hrs, min, sec)
		if self.tzhrs() < 0:
			dtstr += " -%02d%02d" % (-self.tzhrs(), self.tzmin())
		else:
			dtstr += " +%02d%02d" % (self.tzhrs(), self.tzmin())
		return dtstr
	
	def localhms(self):
		(year, mon, day, hrs, min, sec, x, y, z) = time.gmtime(self.__tm + self.__timezone)
		return HMS(hrs + (min / 60) + (sec / 3600))

	def time(self):
		return HMS((self.__tm % 86400) / 3600)

	def JD(self):
		return (self.__tm / 86400) + 2440587.5

	def LST(self, earthpos):
		lst = 100.46 + 0.985647 * self.days_since_y2k() + earthpos.longitude().value() + 15 * self.time().value()
		lst %= 360
		lst /= 15
		return HMS(lst)

	def __iadd__(self, other):
		self.__tm += other
		return self

	def __sub__(self, other):
		return (self.__tm - other.__tm) / 3600

