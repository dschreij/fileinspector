# -*- coding: utf-8 -*-

"""
This file is part of fileinspector.

fileinspector is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

fileinspector is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with fileinspector.  If not, see <http://www.gnu.org/licenses/>.

Created on Wed Mar  2 11:37:36 2016

@author: Daniel Schreij
"""


# Python3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__version__ = '1.0.2'

import sys
import mimetypes
import warnings

try:
	import magic
except ImportError as e:
	warnings.warn("python-magic could not be imported so its features will be "
	"unavailable.\n{}".format(e), ImportWarning)
	magic = None

def determine_category(mimetype):
	""" Determines the category to which the file can be attributed.

	Parameters
	----------
	mimetype : string
		The mimetype specified as <type>/<subtype>

	Returns
	-------
	string : the category or None if no match was found.
	"""

	if 'image' in mimetype:
		return 'image'
	elif 'pdf' in mimetype:
		return 'pdf'
	elif "text/x-" in mimetype:
		return 'code'
	elif "text/plain" in mimetype:
		return 'text'
	elif "msword" in mimetype or \
		"officedocument.wordprocessingml" in mimetype or \
		"opendocument.text" in mimetype:
		return 'doc'
	elif "powerpoint" in mimetype or \
		"presentation" in mimetype:
		return 'presentation'
	elif "excel" in mimetype or \
		"spreadsheet" in mimetype:
		return 'spreadsheet'
	elif "zip" in mimetype or "x-tar" in mimetype\
		or "compressed" in mimetype:
		return 'archive'
	elif "video" in mimetype:
		return 'video'
	elif "audio" in mimetype:
		return 'audio'
	# If nothing matched, simply return False
	return None

def determine_type_with_magic(filename, mime=True):
	""" Determines the filetype using the python-magic library.

	Parameters
	----------
	filename : string
		The path to or name of the file (including extension)
	format : string (optional)
		The output format of the function.

		The default is 'mime', in which case the mimetype is returned
		in the format of <type>/<subtype>

		Other options:
		'verbose' for the standard more wordy python-magic description of files.

	Returns
	-------
	string : the mimetype in the specified format.
	"""
	if magic is None:
		raise ImportError("python-magic is not available. This function cannot be used")
	try:
		ftype = magic.from_file(filename,mime=mime)
	# In some cases, magic doesn't have the from_file() function, which is why
	# we also catch AttributeErrors.
	except (IOError, AttributeError):
		ftype = None

	if type(ftype) == bytes:
		ftype = ftype.decode('utf-8')
	return ftype

def determine_type_with_mimetypes(filename):
	""" Determines the filetype using mimetypes.

	Parameters
	----------
	filename : string
		The path to or name of the file (including extension)

	Returns
	-------
	string : the determined mimetype as <type>/<subtype> or False if no type
	could be determined.
	"""
	mime, encoding = mimetypes.guess_type(filename)
	return mime


def determine_type(filename, output="mime"):
	""" Determines the filetype. Tries to use python-magic first, but if this
	doesn't work out (because the file for instance cannot be accessed locally,
	or python-magic is not available for other reasons), it falls back to the
	mimetypes modules, which uses the filename + extension to make an educated
	guess about the filetype.

	Parameters
	----------
	filename : string
		The path to or name of the file (including extension)
	format : string (optional)
		The output format of the function.

		The default is 'mime', in which case the mimetype is returned
		in the format of <type>/<subtype>

		Other options are:

		- 'xdg' for a freedesktop specification (<type>-<subtype>).
		- 'verbose' for the standard python-magic output, if the module is \
		available. If not, it defaults back to 'mime'

	Returns
	-------
	found_type : string/boolean
		the mimetype in the specified format or None if nothing could be found.
	"""
	# Initialize ftype as None
	ftype = None

	# First try to use python-magic to determine the filetype, as it is not
	# fooled by incorrect or absent file extensions.
	# Only do this is python-magic is available
	if not magic is None:
		ftype = determine_type_with_magic(filename, (output!="verbose") )

	# If python-magic is not available, or it could not determine the filetype,
	# use mimetypes
	if ftype == None:
		ftype = determine_type_with_mimetypes(filename)

	# freedesktop doesn't use <type>/<subtype> but <type>-<subtype> as mime
	# format. Translate if requested.
	if output=="xdg" and not ftype is None:
		ftype = translate_to_xdg(ftype)

	return ftype

def translate_to_xdg(mimetype):
	""" Translates the mimetype into the xdg format of
	<type>-<subtype>.

	Parameters
	----------
	mimetype : string
		The specified mimetype specified as <type>/<subtype>

	Returns
	-------
	xdg-type : string
		the mimetype translated to freedesktop.org format
	"""
	return mimetype.replace("/","-")

__all__ = ['translate_to_xdg', 'determine_type', 'determine_type_with_mimetypes',
'determine_type_with_magic', 'determine_category']

if __name__ == "__main__":
	import os
	if len(sys.argv) < 2:
		files = filter(lambda x: not x in [".",".."], os.listdir("."))
		print("Inspecting files in current folder.\nYou can also check specific files"
			" by passing them as arguments.\n")
	else:
		files = sys.argv[1:]

	for f in files:
		f_full = os.path.abspath(f)
		if(os.path.isdir(f_full)):
			continue
		print("{}:\t\t{}".format(f, determine_type(f_full,'verbose')))
