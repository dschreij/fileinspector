# File Inspector

Copyright 2016 Daniel Schreij

## About

This module is a layer on top of the standard Python mimetypes module and [python-magic](https://github.com/ahupp/python-magic). Python-magic only works with local files to which you need to have access, while mimetypes only uses the filename to determine its filetype.

File inspector first checks if a file exists at the provided path, and if this is the case it uses python-magic to get more information about the file type. If this is not the case (for instance if you just have a reference uri to an online file, without access to the file itself) the mimetypes module is used to deterimine the filetype based on the filename.

The idea is to then provide uniform mimetype output of the filetype, regardless of the way (mimetypes or python-magic) with which it was determined.

It's a simple as that, nothing fancy here  ;)

## Usage

TODO

## License

`python-filespector` is licensed under the [GNU General Public License
v3](http://www.gnu.org/licenses/gpl-3.0.en.html).
