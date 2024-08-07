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

import datetime
import pytz
import calendar

class Time():
	# 2000-01-01 12:00:00 UTC
	_y2000_timet = 946728000

	def __init__(self, time_utc):
		assert(isinstance(time_utc, datetime.datetime))
		self._time_utc = time_utc

	@property
	def time(self):
		return self._time_utc.hour + (self._time_utc.minute / 60) + (self._time_utc.second / 3600) + (self._time_utc.microsecond / 3600 / 1e6)

	@classmethod
	def from_localtime(cls, local_time, timezone_str):
		assert(isinstance(local_time, datetime.datetime))
		timezone =  pytz.timezone(timezone_str)
		local_time = timezone.localize(local_time)
		utc_time_with_zone = local_time.astimezone(pytz.utc)
		utc_time = utc_time_with_zone.replace(tzinfo = None)
		return cls(utc_time)

	def json(self, timezone_name = None):
		result = {
			"timet":	self.timet,
			"ts_utc":	self.format_in_timezone(),
		}
		if timezone_name is not None:
			result["ts_local"] = self.format_in_timezone(timezone_name)
		return result

	def format_in_timezone(self, timezone_name = None):
		if timezone_name is not None:
			local_ts = pytz.utc.localize(self._time_utc).astimezone(pytz.timezone(timezone_name))
		else:
			local_ts = self._time_utc
		return local_ts.strftime("%Y-%m-%d %H:%M:%S")

	@classmethod
	def from_localtime_str(cls, local_time_str, timezone_str):
		return cls.from_localtime(datetime.datetime.strptime(local_time_str, "%Y-%m-%d %H:%M:%S"), timezone_str)

	@classmethod
	def from_str(cls, time_str):
		return cls(datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%SZ"))

	@classmethod
	def from_timet(cls, timet):
		return cls(datetime.datetime.utcfromtimestamp(timet))

	@classmethod
	def from_jd(cls, jd):
		timet = (jd - 2440587.5) * 86400
		return cls.from_timet(timet)

	@classmethod
	def now(cls):
		return cls(datetime.datetime.utcnow())

	@property
	def days_since_y2000(self):
		"""Returns the days since J2000.0 (2000-01-01 12:00:00 UTC)."""
		return (self.timet - self._y2000_timet) / 86400

	@property
	def jcent_since_y2000(self):
		"""Returns the Julian centuries since J2000.0 (2000-01-01 12:00:00
		UTC)."""
		return self.days_since_y2000 / 36525

	@property
	def timet(self):
		"""Returns the time_t representation of the timestamp (seconds since
		the Epoch)."""
		return calendar.timegm(self._time_utc.utctimetuple())

	@property
	def jd(self):
		"""Returns the Julian date representation of the timestamp."""
		return (self.timet / 86400) + 2440587.5

	@property
	def greenwich_mean_sidereal_time_deg(self):
		"""Returns GMST (Greenwich Mean Sidereal Time) in degrees, as described
		by Keith Burnett (http://www2.arnes.si/~gljsentvid10/sidereal.htm)."""
		gmst_deg = 280.46061837 + (360.98564736629 * self.days_since_y2000) + (0.000388 * (self.jcent_since_y2000 ** 2))
		return gmst_deg % 360

	def local_mean_sidereal_time_deg(self, observer):
		return (self.greenwich_mean_sidereal_time_deg + observer.longitude) % 360

	def local_mean_sidereal_time_hrs(self, observer):
		return self.local_mean_sidereal_time_deg(observer) / 15

	def __str__(self):
		return "Time<%s>" % (self._time_utc.strftime("%Y-%m-%d %H:%M:%S UTC"))

if __name__ == "__main__":
	t = Time.now()
	print(t.timet)
	print(t.jd)
	print(t.days_since_y2000)
