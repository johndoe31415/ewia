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

import sys

class Table():
	def __init__(self, cols, seperators, output = sys.stdout):
		self.__cols = cols
		self.__seps = seperators
		if len(self.__seps) - 1 != len(self.__cols):
			raise Exception("Must have one more seperator than column.")
		self.__quiet = False
		self.__output = output

	def quiet(self):
		self.__quiet = True

	def put(self, entry):
		if self.__quiet:
			return

		if len(entry) != len(self.__cols):
			raise Exception("Need to have %d colums, you provided %d." % (len(self.__cols), len(entry)))
		
		entrystr = ""
		if self.__seps[0] is not None:
			entrystr += self.__seps[0]

		for i in range(len(self.__cols)):
			entrystr += self.__cols[i] % (entry[i])
			if self.__seps[i + 1] is not None:
				entrystr += self.__seps[i + 1]
	
		entrystr += "\n"
		self.__output.write(entrystr)
