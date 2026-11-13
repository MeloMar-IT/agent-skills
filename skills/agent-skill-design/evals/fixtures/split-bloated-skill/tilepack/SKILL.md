---
name: tilepack
description: Builds, verifies and publishes map tile packs with the tilepack CLI. Use when packaging tiles; not for rendering maps (use map-render).
---

# tilepack

Packages rendered map tiles into a distributable pack.

## Workflow

1. Collect the rendered tiles in one input directory.
2. Choose the zoom range for the pack.
3. Pick an output format.
4. Run `tilepack build` with the flags you need.
5. Inspect the manifest the build wrote.
6. Check the pack size against the limit.
7. Run `tilepack verify` on the output.
8. Fix any error the verifier prints.
9. Rebuild after each fix.
10. Compare checksums with the previous release.
11. Tag the pack with a version.
12. Choose the target bucket.
13. Run `tilepack publish` for the pack.
14. Wait for the upload to finish.
15. Fetch the published manifest.
16. Compare it with the local manifest.
17. Record the publication in the release log.
18. Notify the map team.
19. Clear the local cache directory.
20. Archive the build log.
21. Remove temporary files.
22. Close the ticket.

## Flags

| Flag | Meaning |
|------|---------|
| --input | Source directory of rendered tiles |
| --output | Output directory for the pack |
| --format | Pack format, for example mbtiles or folder |
| --zoom-min | Lowest zoom level included |
| --zoom-max | Highest zoom level included |
| --split | Split the pack into several files |
| --overwrite | Replace an existing pack |
| --checksum | Write a checksum file next to the pack |
| --bucket | Target bucket for publishing |
| --prefix | Key prefix inside the bucket |
| --threads | Number of worker threads |
| --tile-size | Tile edge length in pixels |
| --scale | Scale factor for high-density tiles |
| --crs | Coordinate reference system |
| --bbox | Bounding box to include |
| --clip | Clip tiles to the bounding box |
| --buffer | Extra border around the bounding box |
| --simplify | Simplify vector geometry |
| --quality | Image quality from 1 to 100 |
| --compress | Compression method |
| --level | Compression level |
| --dither | Dither palette images |
| --palette | Palette file for indexed tiles |
| --background | Background colour for empty areas |
| --transparent | Keep transparency in tiles |
| --metadata | Extra metadata file |
| --attribution | Attribution text |
| --name | Pack name |
| --description | Pack description |
| --version | Pack version string |
| --schema | Schema file used for validation |
| --index | Write a tile index |
| --manifest | Manifest file path |
| --verbose | Print detailed progress |
| --quiet | Print errors only |
| --log-file | Write the log to a file |
| --dry-run | Show what would happen |
| --resume | Continue an interrupted build |
| --retries | Retry count for uploads |
| --timeout | Network timeout in seconds |
| --cache-dir | Cache directory |
| --temp-dir | Temporary directory |
| --max-size | Largest allowed file in megabytes |
| --min-size | Smallest allowed tile in bytes |
| --skip-empty | Skip empty tiles |
| --fill-empty | Fill empty tiles with the background |
| --sort | Sort order of tiles in the pack |
| --reverse | Reverse the sort order |
| --include | Include pattern |
| --exclude | Exclude pattern |
| --filter | Filter expression |
| --layer | Layer to include |
| --style | Style file |
| --lang | Label language |
| --label | Label field |
| --tag | Tag added to the pack |
| --region | Bucket region |
| --acl | Access policy for uploaded files |
| --signature | Sign the pack with a key |
| --encrypt | Encrypt the pack |

## Errors

- EX-01: input directory not found
- EX-02: input directory is empty
- EX-03: output directory is not writable
- EX-04: unknown pack format
- EX-05: zoom-min is greater than zoom-max
- EX-06: zoom level out of range
- EX-07: tile size is not a power of two
- EX-08: scale factor not supported
- EX-09: unknown coordinate reference system
- EX-10: bounding box is malformed
- EX-11: bounding box is outside the data
- EX-12: buffer is negative
- EX-13: simplify tolerance is invalid
- EX-14: quality is out of range
- EX-15: unknown compression method
- EX-16: compression level is out of range
- EX-17: palette file not found
- EX-18: palette has too many colours
- EX-19: background colour is malformed
- EX-20: metadata file is not valid JSON
- EX-21: attribution text is too long
- EX-22: pack name is empty
- EX-23: pack name has illegal characters
- EX-24: version string is malformed
- EX-25: schema file not found
- EX-26: schema validation failed
- EX-27: tile index could not be written
- EX-28: manifest could not be written
- EX-29: manifest is missing a required field
- EX-30: manifest does not match the tiles
- EX-31: log file is not writable
- EX-32: resume state not found
- EX-33: resume state belongs to another build
- EX-34: upload retries exhausted
- EX-35: network timeout
- EX-36: cache directory is not writable
- EX-37: temporary directory is full
- EX-38: pack file exceeds the size limit
- EX-39: tile is smaller than the minimum size
- EX-40: tile is corrupt
- EX-41: duplicate tile in the input
- EX-42: tile coordinates are inconsistent
- EX-43: sort order is unknown
- EX-44: include pattern is invalid
- EX-45: exclude pattern is invalid
- EX-46: filter expression does not parse
- EX-47: layer not found
- EX-48: style file not found
- EX-49: style file is invalid
- EX-50: language code is unknown
- EX-51: label field not found
- EX-52: tag is malformed
- EX-53: bucket does not exist
- EX-54: bucket is not reachable
- EX-55: region is unknown
- EX-56: access policy is not allowed
- EX-57: credentials are missing
- EX-58: credentials have expired
- EX-59: signature key not found
- EX-60: signature could not be created
- EX-61: encryption key not found
- EX-62: encryption failed
- EX-63: pack already exists
- EX-64: pack is locked by another build
- EX-65: checksum file could not be written
- EX-66: checksum mismatch after upload
- EX-67: split produced an empty part
- EX-68: split part exceeds the size limit
- EX-69: split requires an output directory
- EX-70: verifier found missing tiles
- EX-71: verifier found extra tiles
- EX-72: verifier could not read the pack
- EX-73: publish was attempted before verify
- EX-74: publish target equals the source
- EX-75: publish prefix is invalid
- EX-76: remote manifest differs from local
- EX-77: release log is not writable
- EX-78: archive of the build log failed
- EX-79: cleanup could not remove files
- EX-80: internal error, include the log in a report

## Examples

### Example 1: smallest build
```
tilepack build --input tiles --output pack
```
Builds a pack with default settings.

### Example 2: limit the zoom range
```
tilepack build --input tiles --output pack --zoom-min 2 --zoom-max 10
```
Includes zoom levels 2 to 10.

### Example 3: mbtiles format
```
tilepack build --input tiles --output pack --format mbtiles
```
Writes a single mbtiles file.

### Example 4: high zoom
```
tilepack build --input tiles --output pack --zoom-max 18 --split
```
Splits the pack because the highest zoom is large.

### Example 5: checksum
```
tilepack build --input tiles --output pack --checksum
```
Writes a checksum file.

### Example 6: preview
```
tilepack build --input tiles --output pack --dry-run
```
Shows what would be built.

### Example 7: several threads
```
tilepack build --input tiles --output pack --threads 8
```
Uses eight worker threads.

### Example 8: retina tiles
```
tilepack build --input tiles --output pack --tile-size 512 --scale 2
```
Builds high-density tiles.

### Example 9: clip to a region
```
tilepack build --input tiles --output pack --bbox 5,45,10,48 --clip
```
Clips tiles to the box.

### Example 10: border around the box
```
tilepack build --input tiles --output pack --bbox 5,45,10,48 --buffer 2
```
Adds a two-tile border.

### Example 11: image quality
```
tilepack build --input tiles --output pack --quality 80
```
Trades size for quality.

### Example 12: compression
```
tilepack build --input tiles --output pack --compress zstd --level 9
```
Uses strong compression.

### Example 13: palette tiles
```
tilepack build --input tiles --output pack --palette colors.pal --dither
```
Builds indexed tiles with dithering.

### Example 14: transparent background
```
tilepack build --input tiles --output pack --transparent
```
Keeps transparency.

### Example 15: skip empty tiles
```
tilepack build --input tiles --output pack --skip-empty
```
Leaves empty tiles out.

### Example 16: fill empty tiles
```
tilepack build --input tiles --output pack --fill-empty --background ffffff
```
Fills empty tiles with white.

### Example 17: metadata
```
tilepack build --input tiles --output pack --name alps --description "Alps pack" --version 1.2.0
```
Sets the pack identity.

### Example 18: attribution
```
tilepack build --input tiles --output pack --attribution "Map data by the team"
```
Adds attribution text.

### Example 19: index and manifest
```
tilepack build --input tiles --output pack --index --manifest pack/manifest.json
```
Writes an index and a manifest.

### Example 20: logging
```
tilepack build --input tiles --output pack --verbose --log-file build.log
```
Prints details and logs them.

### Example 21: quiet run
```
tilepack build --input tiles --output pack --quiet
```
Prints only errors.

### Example 22: resume
```
tilepack build --input tiles --output pack --resume
```
Continues an interrupted build.

### Example 23: filters
```
tilepack build --input tiles --output pack --include "*.png" --exclude "tmp*" --filter "zoom>3"
```
Selects tiles by pattern.

### Example 24: layers and style
```
tilepack build --input tiles --output pack --layer roads --style day.json --lang de --label name
```
Builds one layer with a style.

### Example 25: sorting
```
tilepack build --input tiles --output pack --sort zoom --reverse
```
Orders tiles by zoom, highest first.

### Example 26: publish
```
tilepack publish --output pack --bucket maps-staging --prefix alps --region eu-west --acl private
```
Uploads to the staging bucket.

### Example 27: network settings
```
tilepack publish --output pack --bucket maps-staging --retries 5 --timeout 60
```
Retries uploads.

### Example 28: signed pack
```
tilepack publish --output pack --bucket maps-staging --signature key.pem --encrypt
```
Signs and encrypts.

### Example 29: directories and sizes
```
tilepack build --input tiles --output pack --cache-dir .cache --temp-dir /tmp/tp --max-size 500 --min-size 20
```
Sets directories and size limits.

### Example 30: schema and tag
```
tilepack build --input tiles --output pack --schema pack.schema --tag nightly --crs EPSG:3857 --simplify 0.5 --metadata extra.json
```
Validates and tags the pack.

## History

- 2019-01: first prototype
- 2019-02: folder output added
- 2019-03: mbtiles output added
- 2019-04: zoom range options
- 2019-05: bounding box support
- 2019-06: first internal release
- 2019-07: clip support
- 2019-08: palette tiles
- 2019-09: dithering
- 2019-10: compression options
- 2019-11: quality setting
- 2019-12: year-end cleanup
- 2020-01: manifest introduced
- 2020-02: index files
- 2020-03: checksum files
- 2020-04: first publish command
- 2020-05: bucket support
- 2020-06: retries for uploads
- 2020-07: timeouts
- 2020-08: resume support
- 2020-09: thread pool
- 2020-10: memory fixes
- 2020-11: log file support
- 2020-12: year-end cleanup
- 2021-01: schema validation
- 2021-02: filters
- 2021-03: layers
- 2021-04: styles
- 2021-05: label languages
- 2021-06: signing
- 2021-07: encryption
- 2021-08: access policies
- 2021-09: regions
- 2021-10: split packs
- 2021-11: size limits
- 2021-12: year-end cleanup
- 2022-01: verifier introduced
- 2022-02: verifier reports extra tiles
- 2022-03: verifier reports missing tiles
- 2022-04: sort orders
- 2022-05: reverse order
- 2022-06: skip empty tiles
- 2022-07: fill empty tiles
- 2022-08: dry runs
- 2022-09: quiet mode
- 2022-10: verbose mode
- 2022-11: cache directory
- 2022-12: year-end cleanup
- 2023-01: temp directory
- 2023-02: version strings
- 2023-03: tags
- 2023-04: attribution
- 2023-05: descriptions
- 2023-06: retina tiles
- 2023-07: tile size option
- 2023-08: buffer option
- 2023-09: simplify option
- 2023-10: crs option
- 2023-11: error catalogue completed
- 2023-12: year-end cleanup

## Notes

- Tile names follow the z/x/y scheme.
- Build logs are plain text.
- Always run `tilepack verify` before `tilepack publish`.
- Packs are plain files and can be copied with any tool.
- Never pass `--overwrite` on the production bucket.
- The default thread count is the number of CPU cores.
- `--zoom-max` above 16 needs `--split`.
- Old packs are kept for 30 days.
