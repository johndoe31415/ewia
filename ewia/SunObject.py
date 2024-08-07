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

import math
from ewia.Tools import MathTools
from ewia.Observer import Observer
from ewia.Time import Time
from ewia.ApparentPosition import ApparentPosition
from ewia.OrbitalElements import OrbitalElements
from ewia.EquatorialCoordObject import EquatorialCoordObject

class SunObject():
	def calculate_equatorial_position(self, observer, obstime):
		assert(isinstance(observer, Observer))
		assert(isinstance(obstime, Time))

		n = obstime.days_since_y2000

		mean_longitude_deg = (280.460 + (0.9856474 * n)) % 360
		mean_anomaly_g_deg = (357.528 + (0.9856003 * n)) % 360

		ecliptic_longitude_lambda_deg = mean_longitude_deg + (1.915 * MathTools.dsin(mean_anomaly_g_deg)) + (0.020 * MathTools.dsin(2 * mean_anomaly_g_deg))

		# Ecliptic latitude beta is assumed to be zero
		distance_sun_earth_R_au = 1.00014 - (0.01671 * MathTools.dcos(mean_anomaly_g_deg)) - (0.00014 * MathTools.dcos(2 * mean_anomaly_g_deg))

		# Earth's obliquity
		obliquity_deg = OrbitalElements.calculate_earth_obliquity_deg(obstime)

		right_ascension_rad = math.atan2(MathTools.dcos(obliquity_deg) * MathTools.dsin(ecliptic_longitude_lambda_deg), MathTools.dcos(ecliptic_longitude_lambda_deg))
		right_ascension_deg = 180 * right_ascension_rad / math.pi
		right_ascension_hrs = (right_ascension_rad * 24 / (2 * math.pi)) % 24

		declination_rad = math.asin(MathTools.dsin(obliquity_deg) * MathTools.dsin(ecliptic_longitude_lambda_deg))
		declination_deg = 180 * declination_rad / math.pi

		equatorial_pos = EquatorialCoordObject(right_ascension_hrs, declination_deg)
		return equatorial_pos

	def calculate_apparent_position(self, observer, obstime):
		equatorial_pos = self.calculate_equatorial_position(observer, obstime)
		return equatorial_pos.calculate_apparent_position(observer, obstime)

	def __str__(self):
		return "Sol"
