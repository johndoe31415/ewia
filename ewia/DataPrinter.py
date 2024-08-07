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

class DataPrinter():
	def __init__(self, observer_name, observer, obs_timestamps, timezone):
		self.__timezone = timezone
		self.__observer_name = observer_name
		self.__observer = observer
		self.__timestamps = obs_timestamps
		self.__objects = [ ]
		self.__apparent_positions = [ ]

	def add_object(self, name, obs_obj):
		self.__objects.append((name, obs_obj))
		self.__apparent_positions.append([ obs_obj.calculate_apparent_position(self.__observer, timestamp) for timestamp in self.__timestamps ])
		return self

	def dump(self):
		if len(self.__timestamps) > 1:
			print("Observer location: %s (%s), times in %s" % (self.__observer_name, self.__observer, self.__timezone))
			print()
		else:
			print("Observer location: %s (%s), at time %s (%s)" % (self.__observer_name, self.__observer, self.__timestamps[0].format_in_timezone(self.__timezone), self.__timezone))
		for ((obs_obj_name, obs_obj), apparent_positions) in zip(self.__objects, self.__apparent_positions):
			if len(self.__timestamps) > 1:
				print("%s" % (obs_obj_name))
				for (timestamp, apparent_position) in zip(self.__timestamps, apparent_positions):
					print("    At %s: Altitude %.1f°, Azimuth %.1f° (%s)" % (timestamp.format_in_timezone(self.__timezone), apparent_position.altitude, apparent_position.azimuth, apparent_position.azimuth_compass))
				print()
			else:
				apparent_position = apparent_positions[0]
				print("    %s: Altitude %.1f°, Azimuth %.1f° (%s)" % (obs_obj_name, apparent_position.altitude, apparent_position.azimuth, apparent_position.azimuth_compass))

	def json(self):
		result = {
			"observer":		self.__observer.json(),
			"timezone":		self.__timezone,
			"timestamps":	[ ts.json(self.__timezone) for ts in self.__timestamps ],
			"observations":	[ ],
		}
		for ((obs_obj_name, obs_obj), apparent_positions) in zip(self.__objects, self.__apparent_positions):
			observation = { }
			observation["obj_name"] = obs_obj_name
			observation["positions"] = [ apparent_position.json() for apparent_position in apparent_positions ]
			result["observations"].append(observation)
		return result
