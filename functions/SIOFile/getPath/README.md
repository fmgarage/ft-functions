# SIOFile.getPath( _path; _format )

## About

Genereate or convert paths for different formats. 

## Parameters

### _path

string input path

Keywords: You can use keywords as alias for tmp, desktop, file, documents, settings, application, extensions.

Examples:

- "desktop/test/export.txt" will output "/Users/yourname/Desktop/test/export.txt" on a Mac

### _format

string output format, default = "os"

os, mac, win, url, troi, file (filemac/filewin), image (imagemac/imagewin)

## Result

Returns the path in the specified format or an error message ("ERROR: …")



## Version History

| Version | Date       | Author | Notes              |
| ------- | ---------- | ------ | ------------------ |
| 1.1.0   | 2015-02-22 | NW     | add format "image" |

