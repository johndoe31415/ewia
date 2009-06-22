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

from DEG import DEG
from RE import RE
class HMS():
	def __init__(self, value):
		if type(value) == float:
			self.__value = value % 24
		else:
			flt = "([0-9]+(?:\.[0-9]*)?)"
			spc = "[ \t]*"
			hms_re = RE("^" + spc + flt + spc + "(?::" + spc + flt + spc + ")?(?::" + spc + flt + spc + ")?")
			if hms_re.match(value):
				self.__value = float(hms_re[1])
				if hms_re[2] is not None:
					self.__value += float(hms_re[2]) / 60
				if hms_re[3] is not None:
					self.__value += float(hms_re[3]) / 3600
			else:
				raise Exception("Could not match %s to [hh:mm:ss] format." % (value))

	def h(self):
		return int(self.__value)
	
	def m(self):
		return int((abs(self.__value) - abs(self.h())) * 60)

	def s(self):
		return round((abs(self.__value) - abs(self.h()) - self.m() / 60) * 3600)

	def negate(self):
		self.__value = -self.__value

	def __str__(self):
		return "%d:%02d:%02d" % (self.h(), self.m(), self.s())

	def __add__(self, addvalue):
		newvalue = (self.__value + addvalue) % 24
		return HMS(newvalue)

	def __lt__(self, other):
		return self.__value < other.__value
	
	def __le__(self, other):
		return self.__value <= other.__value
	
	def __ge__(self, other):
		return self.__value >= other.__value

	def value(self):
		return self.__value

	def dms(self):
		return DEG(self.__value * 15)
