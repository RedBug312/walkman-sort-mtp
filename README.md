# walkman-sort-mtp
Transfer MP3 audio files via MTP in sorted order

## Intro
My Walkman MP3 player (Sony NWZ-B163F) failed reading ID3 tags, the songs inside can only be sorted as uploading order. This script bulkly uploads MP3 audio files in ID3 tags sorted order.

## Usage

```
$ pip install eyed3 tqdm
$ ./upload.py [options] <SOURCE_DIR> <DEVICE_DIR>
```

Note that `<DEVICE_DIR>` should be started with `mtp:/` as its root directory

Options:
* `-s`, `--sort`: sorting criteria with same denotations as eyed3, default is `aAn`
* `-n`, `--no`: print the order of the files but not upload (not implemented)
* `-f`, `--force-after`: overwrite songs on device after new songs
* `-F`, `--force-all`: overwrite all songs on device

You can run `$ ./upload.py -h` for more detailed options explaination.

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

You can find the reference [here](https://bugs.launchpad.net/ubuntu/+source/gvfs/+bug/1314556u)

## Credits
* [eyeD3](http://eyed3.nicfit.net/), Python audio data toolkit
* [mtpy](https://github.com/ldo/mtpy), A more Pythonic interface to libmtp
* [tqdm](https://github.com/tqdm/tqdm), A fast, extensible progress bar for Python and CLI 

## License
This software is licensed under the [GPL v3 license](http://www.gnu.org/copyleft/gpl.html).
