#! /usr/bin/python3
import os
import eyed3
import lib.mtpy as mtpy
import tqdm

# default options
_OPTION = {
    'sort': 'aAn',
    'force': 0,
}

def search_audios(srcdir):
    audiopaths = [os.path.join(root, f) for root, dirs, files in os.walk(srcdir)
                                        for f in files
                                        if os.path.splitext(f)[1] in ('.mp3', '.MP3')]
    audiolist = [{'path': os.path.relpath(path, srcdir),
                  'tags': eyed3.load(path).tag }
                for path in audiopaths]

    tag_getter = {
        'a': lambda audio: audio['tags'].artist or '',
        'A': lambda audio: audio['tags'].album or '',
        'n': lambda audio: audio['tags'].track_num[0] or 0
    }
    reverse = False
    for tag in _OPTION['sort'][::-1]:
        if tag == '-':
            reverse = True
        elif tag not in tag_getter:
            pass
        else:
            audiolist.sort(reverse=reverse, key=tag_getter[tag])
            reverse = False
    return audiolist


def choose_device():
    raw_devs = mtpy.get_raw_devices()
    for index, raw_dev in enumerate(raw_devs):
        print('Device {}: {}'.format(index, repr(raw_dev)))

    choose = -1
    while not 0 <= choose < len(raw_devs):
        choose = int(input('Target device: '))
    return raw_devs[choose]


def upload(audiolist, device, srcdir, dstdir):
    dev = device.open()

    pbar = tqdm.tqdm(audiolist)
    for audio in pbar:
        srcpath = os.path.join(srcdir, audio['path'])
        dstpath = os.path.join(dstdir, audio['path'])
        pbar.set_description(dstpath)

        existed = dev.get_descendant_by_path(dstpath)
        if _OPTION['force'] == 1 and existed is None:
            _OPTION['force'] = 2
        elif _OPTION['force'] == 2 and existed is not None:
            existed.delete()
        elif existed is not None:
            continue

        curr = dev
        for folder in dstpath.split('/')[1:-1]:
            nex4 = curr.get_child_by_name(folder)
            if curr is None:
                curr = curr.create_folder(folder)
            else:
                curr = nex4
        curr.send_file(srcpath)

    dev.close()


def main():
    import sys
    import getopt

    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:fF', ['sort=', 'force-after', 'force-all'])
    except getopt.GetoptError:
        print('Invalid options')
        sys.exit(1)
    else:
        for opt, val in opts:
            if opt in ('-s', '--sort'):
                _OPTION['sort'] = val
            elif opt in ('-f', '--force-after'):
                _OPTION['force'] = 1
            elif opt in ('-F', '--force-all'):
                _OPTION['force'] = 2

    try:
        assert args[1].startswith('mtp:/')
    except (IndexError, AssertionError):
        print('Invalid paths')
        sys.exit(1)
    else:
        srcdir = os.path.expanduser(args[0])
        dstdir = args[1][4:]

    audiolist = search_audios(srcdir)
    device = choose_device()
    upload(audiolist, device, srcdir, dstdir)


if __name__ == '__main__':
    main()
