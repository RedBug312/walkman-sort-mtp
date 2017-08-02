# walkman-sort-mtp
A python script to upload sorted MP3 audio files via MTP

## Intro
My Walkman MP3 player (Sony NWZ-B163F) failed reading ID3 tags, the songs inside can only be sorted as uploading order. I have to upload them one-by-one since Bash script does not work on MTP.

For this situation, this script will uploads all the MP3 audio files in your Music folder, which are already sorted by ID3 tags in the audio files.

## Usage

```
$ pip install eyed3 tqdm
$ ./upload.py [options] <SOURCE_DIR> <DEVICE_DIR>
```

Note that `<DEVICE_DIR>` should be started with `mtp:/` as its root directory.

Options:
* `-s`, `--sort`: order of sorting criteria [default: bGYAn]
* `-n`, `--no`: print the order of the files, but not upload them
* `-f`, `--force-after`: overwrite songs on device after new songs uploaded
* `-F`, `--force-all`: overwrite all songs on device

Sorting criteria:
* `a`: artist name
* `A`: album name
* `b`: album artist name
* `t`: track title
* `n`: track number
* `N`: total number of tracks
* `d`: disc number
* `D`: total number of discs in set
* `G`: genre id
* `Y`: releasing year
* `-`: reverse the order of previous criteria

You can run `$ ./upload.py --help` for a more detailed options explaination.

Demo:
[![asciicast](https://asciinema.org/a/0IvJu8h9RHpYABqFgamSFEBQt.png)](https://asciinema.org/a/0IvJu8h9RHpYABqFgamSFEBQt)

## FAQ
### I get `PTP_ERROR_IO` error with the messages below:
```
ignoring libusb_claim_interface() = -6PTP_ERROR_IO: failed to open session, trying again after resetting USB interface
LIBMTP libusb: Attempt to reset device
inep: usb_get_endpoint_status(): Device or resource busy
outep: usb_get_endpoint_status(): Device or resource busy
ignoring libusb_claim_interface() = -6LIBMTP PANIC: failed to open session on second attempt
Unable to open raw device 0
```

Try this in a terminal:
```
$ killall gvfs-gphoto2-volume-monitor
$ killall gvfs-mtp-volume-monitor
```
You can find the reference [here](https://bugs.launchpad.net/ubuntu/+source/gvfs/+bug/1314556u).

## Credits
* [eyeD3](http://eyed3.nicfit.net/), Python audio data toolkit.
* [mtpy](https://github.com/ldo/mtpy), A more Pythonic interface to libmtp.
* [tqdm](https://github.com/tqdm/tqdm), A fast, extensible progress bar for Python and CLI.

## License
This software is licensed under the [GPL v3 license](http://www.gnu.org/copyleft/gpl.html) © RedBug312.
