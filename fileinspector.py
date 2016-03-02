# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:37:36 2016

@author: daniel
"""
import sys
import mimetypes
import logging

try:
	import magic
except ImportError as e:
	print("WARNING: python-magic could not be imported so its features will be \
	unavailable.\n{}".format(e), file=sys.stderr)
	magic = None

def determine_category(mimetype):
	""" Determines the category to which the file can be attributed.

	Parameters
	----------
	mimetype : string
		The mimetype specified as <type>/<subtype>

	Returns
	-------
	string : the category or False if no match was found.
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
	return False

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
		raise ImportError("python-magic is not available. This function cannot \
			be used")
	try:
		ftype = magic.from_file(filename,mime=mime)
	except OSError as e:
		logging.warning("Python-magic could not assess the file: {}".format(e))
		ftype = False

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
	if mime is None:
		return False
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
		the mimetype in the specified format or False if nothing could be found.
	"""
	# Initialize ftype as false
	ftype = False

	# First try to use python-magic to determine the filetype, as it is not
	# fooled by incorrect or absent file extensions.
	# Only do this is python-magic is available
	if not magic is None:
		ftype = determine_type_with_magic(filename, (output!="verbose") )

	# If python-magic is not available, or it could not determine the filetype,
	# use mimetypes
	if ftype == False:
		ftype = determine_type_with_mimetypes(filename)

	# freedesktop doesn't use <type>/<subtype> but <type>-<subtype> as mime
	# format. Translate if requested.
	if output=="xdg":
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
