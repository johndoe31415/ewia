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

class Compass():
	__directions = {
		0:		"N",
		45:		"NE",
		90:		"E",
		135:	"SE",
		180:	"S",
		225:	"SW",
		270:	"W",
		315:	"NW",
		360:	"N",
	}
	__module = 360

	def direction(angle):
		keys = list(Compass.__directions.keys())
		diff = [ abs(key - angle) for key in keys ]
		minidx = min((n, i) for i, n in enumerate(diff))[1]
		return Compass.__directions[keys[minidx]]
