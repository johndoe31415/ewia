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

class SkyCatalog():
	__objects = {
			# Deep Sky
			"Helix Nebula": ("22:29:36.0", "-20° 50' 00''"),
			"Omega Nebula": ("18:20:48.0", "-16° 11' 00''"),
			"sigma Sgr":	("18:55:15.9", "-26° 17' 48.3''"),
			"beta Crv":		("12:34:23.2", "-23° 26' 56''"),
			"Altair":		("19:50:47.0", "8° 52' 6.3''"),
			"Atria":		("16:48:39.9", "-69° 1' 40.1''"),
			"M1":			("05:34.5", "+22° 01'"),
			"M2":			("21:33.5", "-00° 49'"),
			"M3":			("13:42.2", "+28° 23'"),
			"M4":			("16:23.6", "-26° 32'"),
			"M5":			("15:18.6", "+02° 05'"),
			"M6":			("17:40.1", "-32° 13'"),
			"M7":			("17:53.9", "-34° 49'"),
			"M8":			("18:03.8", "-24° 23'"),
			"M9":			("17:19.2", "-18° 31'"),
			"M10":			("16:57.1", "-04° 06'"),
			"M11":			("18:51.1", "-06° 16'"),
			"M12":			("16:47.2", "-01° 57'"),
			"M13":			("16:41.7", "+36° 28'"),
			"M14":			("17:37.6", "-03° 15'"),
			"M15":			("21:30.0", "+12° 10'"),
			"M16":			("18:18.8", "-13° 47'"),
			"M17":			("18:20.8", "-16° 11'"),
			"M18":			("18:19.9", "-17° 08'"),
			"M19":			("17:02.6", "-26° 16'"),
			"M20":			("18:02.6", "-23° 02'"),
			"M21":			("18:04.6", "-22° 30'"),
			"M22":			("18:36.4", "-23° 54'"),
			"M23":			("17:56.8", "-19° 01'"),
			"M24":			("18:16.9", "-18° 29'"),
			"M25":			("18:31.6", "-19° 15'"),
			"M26":			("18:45.2", "-09° 24'"),
			"M27":			("19:59.6", "+22° 43'"),
			"M28":			("18:24.5", "-24° 52'"),
			"M29":			("20:23.9", "+38° 32'"),
			"M30":			("21:40.4", "-23° 11'"),
			"M31":			("00:42.7", "+41° 16'"),
			"M32":			("00:42.7", "+40° 52'"),
			"M33":			("01:33.9", "+30° 39'"),
			"M34":			("02:42.0", "+42° 47'"),
			"M35":			("06:08.9", "+24° 20'"),
			"M36":			("05:36.1", "+34° 08'"),
			"M37":			("05:52.4", "+32° 33'"),
			"M38":			("05:28.4", "+35° 50'"),
			"M39":			("21:32.2", "+48° 26'"),
			"M40":			("12:22.4", "+58° 05'"),
			"M41":			("06:46.0", "-20° 44'"),
			"M42":			("05:35.4", "-05° 27'"),
			"M43":			("05:35.6", "-05° 16'"),
			"M44":			("08:40.1", "+19° 59'"),
			"M45":			("03:47.0", "+24° 07'"),
			"M46":			("07:41.8", "-14° 49'"),
			"M47":			("07:36.6", "-14° 30'"),
			"M48":			("08:13.8", "-05° 48'"),
			"M49":			("12:29.8", "+08° 00'"),
			"M50":			("07:03.2", "-08° 20'"),
			"M51":			("13:29.9", "+47° 12'"),
			"M52":			("23:24.2", "+61° 35'"),
			"M53":			("13:12.9", "+18° 10'"),
			"M54":			("18:55.1", "-30° 29'"),
			"M55":			("19:40.0", "-30° 58'"),
			"M56":			("19:16.6", "+30° 11'"),
			"M57":			("18:53.6", "+33° 02'"),
			"Ring Nebula":	("18:53.6", "+33° 02'"),
			"M58":			("12:37.7", "+11° 49'"),
			"M59":			("12:42.0", "+11° 39'"),
			"M60":			("12:43.7", "+11° 33'"),
			"M61":			("12:21.9", "+04° 28'"),
			"M62":			("17:01.2", "-30° 07'"),
			"M63":			("13:15.8", "+42° 02'"),
			"M64":			("12:56.7", "+21° 41'"),
			"M65":			("11:18.9", "+13° 05'"),
			"M66":			("11:20.2", "+12° 59'"),
			"M67":			("08:50.4", "+11° 49'"),
			"M68":			("12:39.5", "-26° 45'"),
			"M69":			("18:31.4", "-32° 21'"),
			"M70":			("18:43.2", "-32° 18'"),
			"M71":			("19:53.8", "+18° 47'"),
			"M72":			("20:53.5", "-12° 32'"),
			"M73":			("20:58.9", "-12° 38'"),
			"M74":			("01:36.7", "+15° 47'"),
			"M75":			("20:06.1", "-21° 55'"),
			"M76":			("01:42.4", "+51° 34'"),
			"M77":			("02:42.7", "-00° 01'"),
			"M78":			("05:46.7", "+00° 03'"),
			"M79":			("05:24.5", "-24° 33'"),
			"M80":			("16:17.0", "-22° 59'"),
			"M81":			("09:55.6", "+69° 04'"),
			"M82":			("09:55.8", "+69° 41'"),
			"M83":			("13:37.0", "-29° 52'"),
			"M84":			("12:25.1", "+12° 53'"),
			"M85":			("12:25.4", "+18° 11'"),
			"M86":			("12:26.2", "+12° 57'"),
			"M87":			("12:30.8", "+12° 24'"),
			"M88":			("12:32.0", "+14° 25'"),
			"M89":			("12:35.7", "+12° 33'"),
			"M90":			("12:36.8", "+13° 10'"),
			"M91":			("12:35.4", "+14° 30'"),
			"M92":			("17:17.1", "+43° 08'"),
			"M93":			("07:44.6", "-23° 52'"),
			"M94":			("12:50.9", "+41° 07'"),
			"M95":			("10:44.0", "+11° 42'"),
			"M96":			("10:46.8", "+11° 49'"),
			"M97":			("11:14.8", "+55° 01'"),
			"M98":			("12:13.8", "+14° 54'"),
			"M99":			("12:18.8", "+14° 25'"),
			"M100":			("12:22.9", "+15° 49'"),
			"M101":			("14:03.2", "+54° 21'"),
			"M103":			("01:33.2", "+60° 42'"),
			"M104":			("12:40.0", "-11° 37'"),
			"M105":			("10:47.8", "+12° 35'"),
			"M106":			("12:19.0", "+47° 18'"),
			"M107":			("16:32.5", "-13° 03'"),
			"M108":			("11:11.5", "+55° 40'"),
			"M109":			("11:57.6", "+53° 23'"),
			"M110":			("00:40.4", "+41° 41'"),
	}

	def get(skyobject):
		return SkyCatalog.__objects[skyobject]

	def contains(skyobject):
		return SkyCatalog.__objects.get(skyobject) is not None

