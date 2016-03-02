# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:37:36 2016

@author: daniel
"""

import mimetypes
import magic

def determine_filetype(filename):
	""" Determines the mimetype based on the passed extenstion. 

	Parameters
	----------
	filename : string
		The extension of the file

	Returns
	-------
	string : the mimetype.
	"""
	
	mimetype, encoding = mimetypes.guess_type(filename)
	if mimetype:
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
	return "unknown"