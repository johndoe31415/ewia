import datetime
import pytz
import calendar

class Time(object):
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
		raise Exception(NotImplemented)

	@classmethod
	def from_str(cls, time_str):
		return cls(datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%SZ"))

	@classmethod
	def now(cls):
		return cls(datetime.datetime.utcnow())

	@property
	def days_since_y2000(self):
		"""Returns the days since 2000-01-01 12:00:00 UTC."""
		return (self.timet - self._y2000_timet) / 86400

	@property
	def timet(self):
		"""Returns the time_t representation of the timestamp (seconds since
		the Epoch)."""
		return calendar.timegm(self._time_utc.utctimetuple())

	@property
	def jd(self):
		"""Returns the Julian date representation of the timestamp."""
		return (self.timet / 86400) + 2440587.5

	def local_sidereal_time_deg(self, observer):
		"""Return the local sidereal time in degrees at the given observing
		location."""
		lst = 100.46
		lst += 0.985647 * self.days_since_y2000
		lst += observer.longitude
		lst += 15 * self.time
		return lst % 360


	def local_sidereal_time_hrs(self, observer):
		"""Return the local sidereal time in hours at the given observing
		location."""
		return self.local_sidereal_time_deg(observer) / 15

	def __str__(self):
		return "Time<%s>" % (self._time_utc.strftime("%Y-%m-%d %H:%M:%S UTC"))

if __name__ == "__main__":
	t = Time.now()
	print(t.timet)
	print(t.jd)
	print(t.days_since_y2000)
