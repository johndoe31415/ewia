#   Ewia - A tool to calculate astrophysical object positions.
#   Copyright (C) 2017-2017 Johannes Bauer
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

import re

class Tools(object):
	_hms_re = re.compile("(?P<hrs>\d{1,2}):(?P<minutes>\d{2}):(?P<seconds>\d{2}(\.\d*)?)")
	_deg_res = { }

	@classmethod
	def parse_hms(cls, text):
		result = cls._hms_re.fullmatch(text)
		if result is None:
			raise Exception("Cannot parse '%s' as hour:minutes:seconds value." % (text))
		return float(result["hrs"]) + (float(result["minutes"]) / 60) + (float(result["seconds"]) / 3600)

	@classmethod
	def _compile_deg_regex(cls, negative_prefix, positive_prefix):
		regex_text = r"(?P<sign>[" + negative_prefix + positive_prefix + "])\s*"
		regex_text += "("
		regex_text += r"(?P<deg_float>\d+(\.\d*)?)\s*°?"
		regex_text += "|"
		regex_text += r"(?P<deg_int>\d+)\s*°(\s*(?P<min_int>\d+)\s*'(\s*(?P<sec_float>\d+(\.\d*)?)\s*'')?)?"
		regex_text += ")"
		return re.compile(regex_text)

	@classmethod
	def _get_deg_regex(cls, negative_prefix, positive_prefix):
		assert(isinstance(str, negative_prefix))
		assert(isinstance(str, positive_prefix))
		key = (negative_prefix, positive_prefix)
		if key not in cls._deg_res:
			cls._deg_res[key] = self._compile_deg_regex(negative_prefix, positive_prefix)
		return cls._deg_res[key]

	@classmethod
	def parse_deg(cls, negative_prefix, positive_prefix, text):
		regex = self._get_deg_regex(negative_prefix, positive_prefix)
		result = regex.fullmatch(text)
		if result is None:
			raise Exception("Cannot parse '%s'." % (text))

		result = result.groupdict()
		if result["deg_float"] is not None:
			fresult = float(result["deg_float"])
		else:
			fresult = float(result["deg_int"])
			if result["min_int"] is not None:
				fresult += float(result["min_int"]) / 60
			if result["sec_float"] is not None:
				fresult += float(result["sec_float"]) / 3600
		if result["sign"] in negative_prefix:
			fresult = -fresult
		return fresult

