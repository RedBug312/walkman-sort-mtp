#! /usr/bin/python3
"""! @package walkmansortmtp
@file main.py
@author RedBug312
@date Jul 2017
"""
import os
import eyed3
import lib.mtpy as mtpy
import tqdm

__version__ = '1.0'

def search_audios(srcdir):
    """! Search all audio files (*.mp3) under the folder.
    @param srcdir the folder to search from
    @return all audio files listed in given order
    """
    audiopaths = [os.path.join(root, f) for root, _, files in os.walk(srcdir)
                                        for f in files
                                        if os.path.splitext(f)[1] in ('.mp3', '.MP3')]
    audiolist = [{'path': os.path.relpath(path, srcdir),
                  'tags': eyed3.load(path).tag }
                for path in audiopaths]

    tag_getter = {
        'a': lambda audio: audio['tags'].artist or '',
        'A': lambda audio: audio['tags'].album or '',
        'b': lambda audio: audio['tags'].album_artist or '',
        't': lambda audio: audio['tags'].title or '',
        'n': lambda audio: audio['tags'].track_num[0] or 0,
        'N': lambda audio: audio['tags'].track_num[1] or 0,
        'd': lambda audio: audio['tags'].disc_num[0] or 0,
        'D': lambda audio: audio['tags'].disc_num[1] or 0,
        'G': lambda audio: audio['tags'].genre or 0,
        'Y': lambda audio: audio['tags'].getBestDate() or None,
    }
    reverse = False
    for tag in OPTS.sort[::-1]:
        if tag == '-':
            reverse = True
        elif tag not in tag_getter:
            pass
        else:
            audiolist.sort(reverse=reverse, key=tag_getter[tag])
            reverse = False
    return audiolist


def choose_device():
    """! An interactive CLI interface only ask user to choose the device.
    @return the chosen raw device
    """
    raw_devs = mtpy.get_raw_devices()
    for index, raw_dev in enumerate(raw_devs):
        print('Device {}: {}'.format(index, repr(raw_dev)))

    choose = -1
    while not 0 <= choose < len(raw_devs):
        choose = int(input('Target device: '))
    return raw_devs[choose]


def upload(audiolist, device, srcdir, dstdir):
    """! Upload all the audio files to device.
    The path follows: /SRCDIR/path/to/audio.mp3 -> /DSTDIR/path/to/audio.mp3
    @param audiolist the audio files to upload
    @param device the raw device to upload to
    @param srcdir the base folder in local to upload from
    @param dstdir the base folder in device to upload to
    @return the sum of files uploaded successfully
    """
    dev = device.open()
    success_num = 0

    pbar = tqdm.tqdm(audiolist) if OPTS.action else audiolist
    for audio in pbar:
        srcpath = os.path.join(srcdir, audio['path'])
        dstpath = os.path.join(dstdir, audio['path'])
        if OPTS.action:
            pbar.set_description(dstpath)

        existed = dev.get_descendant_by_path(dstpath)
        if OPTS.force == 1 and existed is None:
            OPTS.force = 2
        elif OPTS.force == 2 and OPTS.action and existed is not None:
            existed.delete()
        elif OPTS.force != 2 and existed is not None:
            continue

        if OPTS.action:
            curr = dev
            for folder in dstpath.split('/')[1:-1]:
                nex4 = curr.get_child_by_name(folder)
                curr = curr.create_folder(folder) if nex4 is None else nex4
            if curr.send_file(srcpath) is not None:
                success_num += 1
        else:
            print('{}: {}'.format(success_num + 1, dstpath))
            success_num += 1

    dev.close()
    return success_num


def main():
    """! The entry point.
    Helps receiving the options and arguments.
    """
    from optparse import OptionParser

    parser = OptionParser(usage='%prog [options] SOURCE_DIR DEVICE_DIR',
                          version='%prog ' + __version__,
                          epilog='For detailed information, see https://github.com/RedBug312/walkman-sort-mtp')
    parser.add_option('-s', '--sort', metavar='SORT',
                      type='string', dest='sort', default='bGYAn',
                      help='order of sorting criteria [default: bGYAn]')
    parser.add_option('-n', '--no-action',
                      action='store_false', dest='action', default=True,
                      help='print the order of the files, but not upload them')
    parser.add_option('-f', '--force-after',
                      action='store_const', const=1, dest='force',
                      help='overwrite songs on device after new songs uploaded')
    parser.add_option('-F', '--force-all',
                      action='store_const', const=2, dest='force',
                      help='overwrite all songs on device')
    global OPTS
    OPTS, ARGS = parser.parse_args()

    if len(ARGS) != 2:
        parser.error('incorrect number of arguments (must be 2)')
    elif not ARGS[1].startswith('mtp:/'):
        parser.error('DEVICE_DIR should be start with “mtp:/” as its root')
    else:
        srcdir = os.path.expanduser(ARGS[0])
        dstdir = ARGS[1][5:]

    audiolist = search_audios(srcdir)
    device = choose_device()
    upload(audiolist, device, srcdir, dstdir)


if __name__ == '__main__':
    main()
