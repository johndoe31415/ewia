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

from SkyPos import SkyPos
from VectorR3 import VectorR3
from math import sin, cos, pi, sqrt, atan2, asin

# This was taken from the excellent algorithmic description of http://uk.answers.yahoo.com/question/index?qid=20090212065710AA8O01g
# Data of the orbital elements was taken from http://jenab6.livejournal.com/3160.html and http://www.geocities.com/antocjo/uny/orbits.html

class Ephemeris():
	# a:		Semimajor axis of elliptic orbit
	# e:		Eccentricity
	# i:		Inclination against ecliptic
	# Omega:	Longitude of the ascending node
	# omega:	Argument of the perihelion
	# T:		Time of perihelion passage
	# M:		Mass in solar masses
	__orbital_elements = {
		"Earth": {
			"a":		1.00000011,				# AU
			"e":		0.01671022,
			"i":		0.00000087,
			"Omega":	-0.19653524,			# rad
			"omega":	1.99330267,				# rad
			"T":		2454836.125,			# JD
			"M":		3.003468905535e-06,		# M_Sol
		},
		"Jupiter": {
			"a":		5.20336301,				# AU
			"e":		0.04839266,
			"i":		0.02278178,
			"Omega":	1.75503590,				# rad
			"omega":	4.78565267,				# rad
			"T":		2451305.445,			# JD
			"M":		9.545523100900e-04,		# M_Sol
		},
		"Mars": {
			"a":		1.52366231,				# AU
			"e":		0.09341233,
			"i":		0.03229924,
			"Omega":	0.86530876,				# rad
			"omega":	4.99971032,				# rad
			"T":		2454254.482,			# JD
			"M":		3.227137901564e-07,		# M_Sol
		},
		"Mercury": {
			"a":		0.38709893,				# AU
			"e":		0.20563069,
			"i":		0.12225805,
			"Omega":	0.84354677,				# rad
			"omega":	0.50832330,				# rad
			"T":		2454755.654,			# JD
			"M":		1.660147805540e-07,		# M_Sol
		},
		"Neptune": {
			"a":		30.06896348,			# AU
			"e":		0.00858587,
			"i":		0.03087784,
			"Omega":	2.29897719,				# rad
			"omega":	4.76910625,				# rad
			"T":		2408052.845,			# JD
			"M":		5.150067869891e-05,		# M_Sol
		},
		"Pluto": {
			"a":		39.48168677,			# AU
			"e":		0.24880766,
			"i":		0.29917998,
			"Omega":	1.92515873,				# rad
			"omega":	1.98554398,				# rad
			"T":		2447799.934,			# JD
			"M":		6.535619124227e-09,		# M_Sol
		},
		"Saturn": {
			"a":		9.53707032,				# AU
			"e":		0.05415060,
			"i":		0.04336201,
			"Omega":	1.98470186,				# rad
			"omega":	5.91172514,				# rad
			"T":		2452816.300,			# JD
			"M":		2.858126791011e-04,		# M_Sol
		},
		"Uranus": {
			"a":		19.19126393,			# AU
			"e":		0.04716771,
			"i":		0.01343659,
			"Omega":	1.29555581,				# rad
			"omega":	1.68833308,				# rad
			"T":		2439410.280,			# JD
			"M":		4.366246040923e-05,		# M_Sol
		},
		"Venus": {
			"a":		0.72333199,				# AU
			"e":		0.00677323,
			"i":		0.05924887,
			"Omega":	1.33833051,				# rad
			"omega":	0.95735306,				# rad
			"T":		2454657.866,			# JD
			"M":		2.447840731989e-06,		# M_Sol
		},
	}

	# Calculates eccentric anomaly using Danby's method
	def __ecc_anomaly(par, m):
		u1 = m
		while True:
			u0 = u1
			f0 = u0 - par["e"] * sin(u0) - m
			f1 = 1 - par["e"] * cos(u0)
			f2 = par["e"] * sin(u0)
			f3 = par["e"] * cos(u0)
			d1 = -f0 / f1
			d2 = -f0 / ( f1 + d1 * f2 / 2 )
			d3 = -f0 / ( f1 + d1 * f2 / 2 + (d2**2) * f3 / 6 )
			u1 = u0 + d3
			if abs(u1 - u0) < 1e-15:
				break
		u = u1
		return u

	def __calculate_for_obj(par, t):
		# Orbital period
		P_x = 365.256898326 * par["a"] ** 1.5 / (1 + par["M"])

		# Mean anomaly
		m_x = (2 * pi * (t - par["T"]) / P_x) % (2 * pi)
		
		# Find the eccentric anomaly
		u_x = Ephemeris.__ecc_anomaly(par, m_x)
		
		# Find CHPV''' (canonical heliocentric position vector, triple prime)
		chpv3_x = VectorR3(par["a"] * (cos(u_x) - par["e"]),
							par["a"] * sin(u_x) * sqrt(1 - par["e"] ** 2),
							0)
		
		# Rotate the triple-prime position vector by the argument of the parrihelion, ω
		chpv2_x = chpv3_x.rotate_xy(par["omega"])
		
		# Rotate the double-prime position vector by the inclination, i.
		chpv1_x = chpv2_x.rotate_yz(par["i"])
		
		# Rotate the single-prime position vector by the longitude of the ascending node, Ω.
		chpv_x = chpv1_x.rotate_xy(par["Omega"])

		return {
			"P":		P_x,		# Orbital period
			"m":		m_x,		# Mean anomaly
			"u":		u_x,		# Eccentric anomaly
			"chpv":		chpv_x,		# CHPV
			"chpv1":	chpv1_x,	# CHPV'
			"chpv2":	chpv2_x,	# CHPV''
			"chpv3":	chpv3_x,	# CHPV'''
		}
	
	def calculate(skyobject, date):
		t = date.JD()
		
		# Parameters of earth and the other object
		pe = Ephemeris.__orbital_elements["Earth"]
		px = Ephemeris.__orbital_elements[skyobject]

		# Calculations for object
		res_e = Ephemeris.__calculate_for_obj(pe, t)
		res_x = Ephemeris.__calculate_for_obj(px, t)

		# Find the vector difference between the heliocentric position vector of object X and 
		# the heliocentric position vector to Earth.
		d = res_x["chpv"] - res_e["chpv"]

		# Find the current obliquity of Earth.
		epsilon = (23.439282 - 3.563e-7 * (t - 2451543.5)) / 180 * pi

		d1 = d.rotate_yz(epsilon)

		distance = d1.length()

		RA1 = atan2(d1[1], d1[0])
		RA = RA1 * 12 / pi

		DEC = asin(d1[2] / distance) * 180 / pi
		return SkyPos(RA, DEC)

	def contains(skyobject):
		return (Ephemeris.__orbital_elements.get(skyobject) is not None) and (skyobject != "Earth")

