# EXIF Renamer


This is a simple exif based file renamer using a template 
for the new file names.

## Usage

```bash
exif_rename [OPTIONS] TEMPLATE FILES...
```
where `TEMPLATE` is a Python format string where the (named) keys are 
EXIF variables and `path`, `file_name`, `full_file_name`.

EXIF Date variables are converted to `datetime.datetime` objects and thus
their format options can be used.

### Options

 - `verbose/quiet`: Use more verbose output (Default: quiet)
 - `exists`: What to do if the target file already exists. One of
    + keep - Keep the original file. Do not overwrite
    + overwrite - Overwrite the file
    + error - Bail out, exit the program
 - `noop`: Do not rename the files, can be used as a whatif in combination
    with `--verbose`

## Example
Make an album for each date
```bash
exif_rename '{path}/{DateTime:%Y-%m-%d}/{file_name}' *.JPG
```

