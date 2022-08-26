# SVD Files

SVD files from zips in `vendor/` are extracted to this directory before
processing. They are also renamed to lower-case so that the SVD name, the YAML
name, and the Rust source file name all match.

Run `extract.sh` to extract all zips in `vendor/` and rename to lowercase.

Don't commit any SVDs from this directory to git; only the zips in `vendor/`
should be committed.
