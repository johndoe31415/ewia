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

from TimeRange import TimeRange
from Ephemeris import Ephemeris
from SkyCatalog import SkyCatalog
from EarthCatalog import EarthCatalog

import getopt
import sys

class CmdLineOpts():
	def syntax(errmsg = None):
		if errmsg is not None:
			print(errmsg)
			print()
		print("%s [Options]" % (sys.argv[0]))
		print()
		print("Valid options are:")
		print("   -q                  Do not display standard information, be quiet (default is false)")
		print("   -v                  Be more verbose (default is not)")
		print("   -p                  Ouptut in parsable form (default is not)")
		print("   -r                  Perform a rise- and set calculation (default is not to)")
		print("   --rfgran=Minutes    Rise/fall granularity in minutes (default is 5 minutes)")
		print("   --rfwindow=Days     Rise/fall calculation time window in days (default is 1 day)")
		print("   --rfcutoff=Degrees  Rise/fall cutoff in degrees (default is 10°)")
		print("   --ostimewin=From,To Rise/fall time window in which observation is possible")
		print("   --time=Timespec     Select time in ISO format (default is now)")
		print("   --tz=Timezone       Select time zone in hours (default is local timezone when time is now, otherwise 0)")
		print("   --object=Name       Select object from object catalog (either ephemeris or deepsky)")
		print("   --object=RA,DEC     Select object from sky position")
		print("   --location=la,lo    Select observer position by latitude and longitude")
		print("   --location=loc      Select observer position by catalog name")
		print("   --ephwindow=Hours   Recalculate the position of ephemerides every n Hours (default is 6)")
		print("   --help              Display this help page")
		print()
		print("Examples:")
		print("   %s -v -p --object=M100 --location=Bamberg" % (sys.argv[0]))
		print("   %s -p \"--position=12:34:23.2,-23°26'56''\" \"--location=N49°54',E10°54'\"" % (sys.argv[0]))
		print("   %s -r -p --object=Saturn --location=Bamberg --ostimewin=22:00,04:00 --rfgran=1" % (sys.argv[0]))
		sys.exit(1)

	def __init__(self):
		self.__options = {
			"quiet":		False,
			"verbose":		False,
			"parsable":		False,
			"risefall":		False,
			"rfgran":		300,		# Seconds
			"rfwindow":		86400,		# Seconds
			"rfcutoff":		10,			# Degrees
			"time":			None,
			"timezone":		None,
			"object":		None,
			"location":		None,
			"ephemeris":	False,
			"ephwindow":	21600,		# Seconds
			"ostimewin":	None,
		}

		try:
			opts, args = getopt.getopt(sys.argv[1:], "qvpr", [ 
				"rfgran=", 
				"rfwindow=", 
				"rfcutoff=", 
				"time=", 
				"tz=", 
				"object=",
				"location=",
				"help",
				"ostimewin=",
		])
		except getopt.GetoptError as msg:
			CmdLineOpts.syntax(msg)

		if len(args) != 0:
			CmdLineOpts.syntax("Program doesn't require arguments, but you provided %s." % (str(args)))

		for (key, value) in opts:
			if key == "-q":
				self.__options["quiet"] = True
			elif key == "-v":
				self.__options["verbose"] = True
			elif key == "-p":
				self.__options["parsable"] = True
			elif key == "-r":
				self.__options["risefall"] = True
			elif key == "--rfgran":
				self.__options["rfgran"] = int(float(value) * 60)
			elif key == "--rfwindow":
				self.__options["rfwindow"] = int(float(value) * 86400)
			elif key == "--rfcutoff":
				self.__options["rfcutoff"] = int(value)
			elif key == "--time":
				self.__options["time"] = value
			elif key == "--tz":
				self.__options["timezone"] = float(value)
			elif key == "--object":
				if self.__options["object"] is not None:
					CmdLineOpts.syntax("Can only supply one 'object' option.")

				pars = value.split(",")
				if len(pars) == 1:
					if Ephemeris.contains(value):
						self.__options["object"] = value
						self.__options["ephemeris"] = True
					elif SkyCatalog.contains(value):
						self.__options["object"] = SkyCatalog.get(value)
					else:
						CmdLineOpts.syntax("Object '%s' not in either ephemeris nor deepsky catalog." % (value))
				elif len(pars) == 2:
					self.__options["object"] = tuple(pars)
				else:
					CmdLineOpts.syntax("--object only takes one or two parameters, not %d." % (len(pars)))
			elif key == "--location":
				pars = value.split(",")
				if len(pars) == 1:
					if not EarthCatalog.contains(value):
						CmdLineOpts.syntax("Location '%s' not in catalog." % (value))
					self.__options["location"] = EarthCatalog.get(value)
				elif len(pars) == 2:
					self.__options["location"] = tuple(pars)
				else:
					CmdLineOpts.syntax("--location only takes one or two parameters, not %d." % (len(pars)))
			elif key == "--ephwindow":
				self.__options["ephwindow"] = int(float(value) * 60)
			elif key == "--ostimewin":
				pars = value.split(",")
				if len(pars) != 2:
					CmdLineOpts.syntax("Time window needs to have two parameters, 'from' and 'to'.")
				self.__options["ostimewin"] = TimeRange(pars[0], pars[1])
			elif key == "--help":
				CmdLineOpts.syntax()
			else:
				raise Exception("Option '%s' valid but not handled, programming error." % (key))

		if self.__options["object"] is None:
			CmdLineOpts.syntax("No object was selected.")
		elif self.__options["location"] is None:
			CmdLineOpts.syntax("No observer location was selected.")

	def __getitem__(self, key):
		return self.__options[key]

