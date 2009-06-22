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

from RE import RE
class DEG():
	def __init__(self, value):
		if type(value) == float:
			self.__value = value
		else:
			flt = "([0-9]+(?:\.[0-9]*)?)"
			nflt = "([+-])?([0-9]+(?:\.[0-9]*)?)"
			spc = "[ \t]*"
			deg_re = RE("^" + spc + nflt + spc + "°(?:" + spc + flt + spc + "')?(?:" + spc + flt + spc + "'')?")
			if deg_re.match(value):
				self.__value = float(deg_re[2])
				if self.__value < 0:
					neg = True
					self.__value = -self.__value
				if deg_re[3] is not None:
					self.__value += float(deg_re[3]) / 60
				if deg_re[4] is not None:
					self.__value += float(deg_re[4]) / 3600
				if deg_re[1] == "-":
					self.__value = -self.__value
			else:
				raise Exception("Could not match %s to [dd° mm' ss''] format." % (value))

	def d(self):
		return int(self.__value)
	
	def m(self):
		return int((abs(self.__value) - abs(self.d())) * 60)

	def s(self):
		return round((abs(self.__value) - abs(self.d()) - self.m() / 60) * 3600)

	def negate(self):
		self.__value = -self.__value

	def value(self):
		return self.__value

	def __str__(self):
		return "%d°%d'%d''" % (self.d(), self.m(), self.s())

	def rad(self):
		return self.__value / 180 * 3.1415

	def __ge__(self, value):
		return self.__value >= value
