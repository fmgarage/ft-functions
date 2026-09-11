# SIOFile.getPath_v3( _path; _format )

## About

Generates or converts file paths between operating system, URL and FileMaker formats. Handles keywords for standard folders (desktop, tmp, documents, …), FileMaker path prefixes (`file:`, `filemac:`, `imagewin:`, …), Windows network paths and Linux server paths.

## Parameters

### _path, *string*

Input path or keyword. Accepts:

- **Keyword** for a standard folder, optionally followed by a sub path:
  `tmp`, `desktop`, `documents`, `settings`, `application`, `extensions`, `addons`, `home` (or `~`), `file` (folder of the current database)
  e.g. `desktop/export/test.txt`
- **FileMaker path** – must carry its prefix: `file:`, `filemac:`, `filewin:`, `filelinux:`, `image:`, `imagemac:`, `imagewin:`, `imagelinux:`
  e.g. `filemac:/Macintosh HD/Users/name/test.txt`
- **OS path** – macOS (`/Volumes/…`), Windows (`C:\…`, `\\server\share\…`, `//server/share/…`) or Linux
- `--version` returns the version number (e.g. `3007001`)

Empty input returns an empty string.

### _format, *string*, default `os`

Output format:

| Format | Output |
| ------ | ------ |
| `os` | System path of the current platform |
| `mac`, `win` | System path for the given platform |
| `url` | `file://` URL |
| `file` | FileMaker path with `filemac:`, `filewin:` or `filelinux:` prefix for the current platform |
| `filemac`, `filewin`, `filelinux` | FileMaker path for the given platform |
| `image` | FileMaker path with `imagemac:`, `imagewin:` or `imagelinux:` prefix for the current platform |
| `imagemac`, `imagewin`, `imagelinux` | FileMaker image path for the given platform |
| `fmnet` | `fmnet:/` path |

Platform-specific formats (`mac`, `filewin`, …) override the current platform, which allows generating paths for another OS. Trailing slashes are removed.

### Variables

- `$_Db.inVersionMode` – if true, the function returns its version number instead of a result
- `$test_system_volume` – injects the name of the macOS system volume for testing

## Result

The path in the requested format, *string*.

## Errors

Returns an error string prefixed with `ERROR: `, no exception.

- `ERROR: unknown _format '…'. use: os, mac, …` – `_format` is not in the list above
- `ERROR: _path cannot be converted into mac format` – input contains backslashes while targeting macOS

## Examples

    SIOFile.getPath_v3( "tmp"; "os" )                       → /private/tmp/…   (macOS)
    SIOFile.getPath_v3( "tmp"; "os" )                       → C:\Users\name\…\   (Windows)
    SIOFile.getPath_v3( "desktop"; "file" )                 → filemac:/Macintosh HD/Users/name/Desktop
    SIOFile.getPath_v3( "desktop/export/test.txt"; "url" )  → file:///Users/name/Desktop/export/test.txt
    SIOFile.getPath_v3( "/Volumes/Server/file.jpg"; "file" ) → filemac:/Server/file.jpg
    SIOFile.getPath_v3( "filewin:/C:/Data/test.txt"; "os" ) → C:\Data\test.txt

## Dependencies

- FileMaker Pro/Server 19 or later (Linux platform detection); earlier versions untested
- No plugins, no other Custom Functions

## References

- [Claris Help: Creating file paths](https://help.claris.com/en/pro-help/content/creating-file-paths.html)
- Native alternatives since FileMaker 18: `ConvertFromFileMakerPath` / `ConvertToFileMakerPath` (no keywords, no cross-platform generation)

## Known issues

- No output for iOS
- Path conversion fails if the macOS system volume is named `System`
- Illegal characters (e.g. `:`) are not replaced
- `extensions` keyword is not resolved correctly on FileMaker Server

## License

MIT – see [LICENSE](../../../LICENSE)

## Version history

| Version | Date       | Author | Notes |
| ------- | ---------- | ------ | ----- |
| 3.7.1   | 2022-06-08 | NW     | fix `_path` = `file` |
| 3.7.0   | 2021-11-03 | NW     | `addons` keyword |
| 3.6.5   | 2021-08-24 | NW     | version suffix |
| 3.6.4   | 2021-05-24 | NW     | revision, `$test_*` hooks, `file:` prefix |
| 3.6.3   | 2021-04-29 | NW     | version mode |
| 3.6.2   | 2021-03-23 | NW     | fix extensions |
| 3.6.1   | 2021-03-06 | NW     | fix double slashes |
| 3.6.0   | 2021-03-05 | NW     | Linux support |
| 3.5.1   | 2020-01-20 | NW     | fix special folder is network alias |
| 3.5.0   | 2019-10-02 | NW     | extensions |
| 3.4.0   | 2019-09-24 | NW     | removed prefixes, moved to SIOFile |
| 3.3.4   | 2019-02-04 | NW     | fix mac, version mode |
| 3.3.3   | 2018-11-17 | NW     | fix Windows network paths |
| 3.3.2   | 2018-11-13 | NW     | fix Windows `\C:` |
| 3.3.1   | 2018-07-18 | NW     | fix Windows network paths, `be` format deprecated |
| 3.3.0   | 2018-03-25 | NW     | `home` / `~` keyword |
| 3.2.0   | 2018-02-02 | NW     | filemac, filewin, imagemac, imagewin |
| 3.1.0   | 2018-01-22 | NW     | preconditions |
| 3.0.1   | 2018-01-05 | NW     | get drive name by documents path for server |
| 3.0.0   | 2017-03-17 | NW     | revision, no trailing slashes, `~`, extensions |
| 2.0.1   | 2016-09-22 | NW     | fix Windows backslashes |
| 2.0.0   | 2015-11-19 | NW     | keyword + sub folder |
| 1.2.0   | 2015-09-15 | AB     | format `be` (Base Elements plugin) |
| 1.1.0   | 2015-02-22 | NW     | format `image` |
