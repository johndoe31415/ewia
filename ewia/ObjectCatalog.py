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

import json
import os
from .Observer import Observer
from .EquatorialCoordObject import EquatorialCoordObject
from .OrbitalElements import OrbitalElements
from .SunObject import SunObject

class ObjectCatalog():
	def __init__(self):
		self._earth_objs = { }
		self._deepsky_objs = { }
		self._ephemeris_objs = { }

	def get_observer(self, name):
		return self._earth_objs[name]

	def get_object(self, name):
		if name.lower() in [ "sun", "sol" ]:
			return SunObject()
		if name in self._deepsky_objs:
			return self._deepsky_objs[name]
		return self._ephemeris_objs[name]

	def append_from_file(self, filename, fail_on_error = True):
		try:
			with open(filename) as f:
				data = f.read()
		except FileNotFoundError:
			if fail_on_error:
				raise
			else:
				return

		data = json.loads(data)

		for (objname, objdata) in data.get("earth", { }).items():
			pos = Observer.from_data(objdata)
			self._earth_objs[objname] = pos

		for (objname, objdata) in data.get("deepsky", { }).items():
			pos = EquatorialCoordObject.from_data(objdata)
			self._deepsky_objs[objname] = pos

		for (objname, objdata) in data.get("ephemeris", { }).items():
			pos = OrbitalElements.from_data(objdata)
			self._ephemeris_objs[objname] = pos


