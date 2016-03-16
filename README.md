# File Inspector
This module is a layer on top of the standard Python mimetypes module and [python-magic](https://github.com/ahupp/python-magic). Python-magic only works with local files to which you need to have access, while mimetypes only uses the filename to determine its filetype.

File inspector first checks if a file exists at the provided path, and if this is the case it uses python-magic to get more information about the file type. If this is not the case (for instance if you just have a reference uri to an online file, without access to the file itself) the mimetypes module is used to deterimine the filetype based on the filename.

The idea is to then provide uniform mimetype output of the filetype, regardless of the way (mimetypes or python-magic) with which it was determined.

It's a simple as that, nothing fancy here  ;)

## Usage

You can use the utility from the command line.

    python fileinspector.py /path/to/local.pdf

for instance would return

    /path/to/local.pdf:       PDF document, version 1.3

if the file is locally accessible, and the python-magic dependency has been met. If a file is not locally accessible (for instance if the resource is located online), or the python-magic dependency is unmet, fileinspector uses the internal python mimetypes module to determine the filetype. Mimetypes bases its guess on the file's extension.

    python fileinspector.py https://www.google.com/images/nav_logo242.png

should return

    https://www.google.com/images/nav_logo242.png:      image/png

It is also possible to scan entire folders

    python fileinspector.py *
    README.md:      ASCII text, with very long lines
    fileinspector.py:       Python script, ASCII text executable
    fileinspector.pyc:      python 2.7 byte-compiled
    setup.py:       Python script, ASCII text executable
    test.md:        ASCII text

